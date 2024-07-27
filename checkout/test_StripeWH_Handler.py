from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from unittest.mock import patch, Mock
from checkout.webhook_handler import StripeWH_Handler
from checkout.models import Order, OrderLineItem
from profiles.models import UserProfile
from products.models import Product
from django.contrib.auth.models import User
from decimal import Decimal

class StripeWH_HandlerTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
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
            original_bag='{}',
            stripe_pid='test_pid'
        )
        self.handler = StripeWH_Handler(request=HttpRequest())

@patch('checkout.webhook_handler.StripeWH_Handler._send_confirmation_email')
def test_handle_payment_intent_succeeded(self, mock_send_email):
    mock_event = {
        'type': 'payment_intent.succeeded',
        'data': {
            'object': {
                'id': 'pi_1234',
                'metadata': {
                    'bag': '{"1": 1}',
                    'save_info': 'true',
                    'username': 'testuser'
                },
                'shipping': {
                    'name': 'Test User',
                    'phone': '1234567890',
                    'address': {
                        'line1': '123 Test St',
                        'line2': '',
                        'city': 'Test City',
                        'state': 'Test State',
                        'postal_code': '12345',
                        'country': 'US',
                    }
                },
                'latest_charge': 'ch_1J2L3M4N5O6P7Q8R9S0T1U2V',
            }
        }
    }
    mock_stripe_charge = Mock()
    mock_stripe_charge.billing_details = Mock(email='test@example.com')
    mock_stripe_charge.amount = 1000

    with patch('stripe.Charge.retrieve', return_value=mock_stripe_charge):
        response = self.handler.handle_payment_intent_succeeded(mock_event)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(mock_send_email.called)

    def test_handle_payment_intent_payment_failed(self):
        mock_event = {'type': 'payment_intent.payment_failed'}
        response = self.handler.handle_payment_intent_payment_failed(mock_event)
        self.assertEqual(response.status_code, 200)

    def test_handle_event(self):
        mock_event = {'type': 'test_event'}
        response = self.handler.handle_event(mock_event)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Unhandled webhook received', response.content.decode())
