from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile
from products.models import Product
from checkout.models import Order
from django.db import IntegrityError

class ProfileViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        try:
            self.user_profile = UserProfile.objects.get(user=self.user)
        except UserProfile.DoesNotExist:
            self.user_profile = UserProfile.objects.create(user=self.user)
        
        self.product = Product.objects.create(name='Test Product', price=100)
        self.order = Order.objects.create(order_number='12345678', user_profile=self.user_profile)

    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_profile_view_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('profile'), {
            'default_phone_number': '1234567890',
            'default_street_address1': '123 Street',
            'default_town_or_city': 'Test City',
            'default_county': 'Test County',
            'default_postcode': '12345',
            'default_country': 'US',
        })
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.default_phone_number, '1234567890')

    def test_order_history_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('order_history', args=[self.order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertContains(response, f'This is a past confirmation for order number {self.order.order_number}')

    def test_my_orders_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('my_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/my_orders.html')
        self.assertContains(response, self.order.order_number)

    def test_add_review_view_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('add_review', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/add_review.html')

    def test_add_review_view_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('add_review', args=[self.product.id]), {
            'customer_name': 'John Doe',
            'rating': 5,
            'comment': 'Great product!',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after success
