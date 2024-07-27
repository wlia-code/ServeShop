from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from .models import Order, OrderLineItem
from profiles.models import UserProfile
from products.models import Product
from decimal import Decimal
import stripe
import json

class CheckoutViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('10.00'),
            description='Test Description'
        )
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            town_or_city='Test City',
            street_address1='123 Test St',
            original_bag=json.dumps({'1': 1}),
            stripe_pid='test_pid'
        )

    @patch('stripe.PaymentIntent.modify')
    def test_cache_checkout_data(self, mock_modify):
        mock_modify.return_value = None  # Mock the Stripe API call
        response = self.client.post(reverse('cache_checkout_data'), {
            'client_secret': 'pi_1234_secret_5678',
            'save_info': 'true'
        })
        self.assertEqual(response.status_code, 200)

    def test_checkout_view_get(self):
        # Mock bag contents and ensure there's an item in the bag
        session = self.client.session
        session['bag'] = {str(self.product.id): {'items_by_size': {'S': 1}}}
        session.save()
        
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_checkout_view_post(self):
        # Set up a mock bag in the session
        bag = {str(self.product.id): {'items_by_size': {'S': 1, 'M': 2}}}
        session = self.client.session
        session['bag'] = bag
        session.save()

        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'country': 'US',
            'postcode': '12345',
            'town_or_city': 'Test City',
            'street_address1': '123 Test St',
            'street_address2': '',
            'county': 'Test County',
            'client_secret': 'test_secret',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(email='test@example.com').exists())

    def test_checkout_success_view(self):
        response = self.client.get(reverse('checkout_success', args=[self.order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, self.order.order_number)
