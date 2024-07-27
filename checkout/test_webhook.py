from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from checkout.views import webhook
from django.conf import settings
import stripe
from checkout.webhook_handler import StripeWH_Handler

class WebhookTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.endpoint = reverse('webhook')
        self.wh_secret = settings.STRIPE_WH_SECRET
        self.stripe_signature = 'test_signature'
        self.valid_payload = b'{"type": "payment_intent.succeeded"}'
        self.invalid_payload = b'invalid_payload'
        self.mock_request = self.factory.post(
            self.endpoint, data=self.valid_payload, content_type='application/json'
        )

    @patch('stripe.Webhook.construct_event')
    def test_valid_webhook(self, mock_construct_event):
        mock_event = {'type': 'payment_intent.succeeded', 'data': {'object': {}}}
        mock_construct_event.return_value = mock_event

        self.mock_request.META['HTTP_STRIPE_SIGNATURE'] = self.stripe_signature

        response = webhook(self.mock_request)
        self.assertEqual(response.status_code, 200)

    @patch('stripe.Webhook.construct_event', side_effect=ValueError('Invalid payload'))
    def test_invalid_payload(self, mock_construct_event):
        self.mock_request.body = self.invalid_payload
        self.mock_request.META['HTTP_STRIPE_SIGNATURE'] = self.stripe_signature

        response = webhook(self.mock_request)
        self.assertEqual(response.status_code, 400)

    @patch('stripe.Webhook.construct_event', side_effect=stripe.error.SignatureVerificationError('Invalid signature', 'sig'))
    def test_invalid_signature(self, mock_construct_event):
        self.mock_request.META['HTTP_STRIPE_SIGNATURE'] = 'invalid_signature'

        response = webhook(self.mock_request)
        self.assertEqual(response.status_code, 400)

    @patch('stripe.Webhook.construct_event')
    def test_unhandled_event_type(self, mock_construct_event):
        mock_event = {'type': 'unhandled_event', 'data': {'object': {}}}
        mock_construct_event.return_value = mock_event

        self.mock_request.META['HTTP_STRIPE_SIGNATURE'] = self.stripe_signature

        response = webhook(self.mock_request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Unhandled webhook received', response.content.decode())
