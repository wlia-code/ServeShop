from django.test import TestCase
from django.conf import settings  # Import settings from django.conf
from decimal import Decimal
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
from django.contrib.auth.models import User

class OrderModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.product = Product.objects.create(name='Test Product', price=Decimal('10.00'))
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            town_or_city='Test City',
            street_address1='123 Test St',
            street_address2='',
            county='Test County',
            original_bag='{}',
            stripe_pid='testpid12345'
        )

    def test_order_number_is_generated(self):
        self.assertIsNotNone(self.order.order_number)
        self.assertEqual(len(self.order.order_number), 32)

    def test_update_total(self):
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )
        self.order.update_total()
        expected_total = self.product.price * 2
        if expected_total < settings.FREE_DELIVERY_THRESHOLD:
            expected_delivery = expected_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            expected_delivery = 0
        expected_grand_total = expected_total + expected_delivery

        self.assertEqual(self.order.order_total, expected_total)
        self.assertEqual(self.order.delivery_cost, expected_delivery)
        self.assertEqual(self.order.grand_total, expected_grand_total)

    def test_save_method_sets_order_number(self):
        order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            town_or_city='Test City',
            street_address1='123 Test St',
            street_address2='',
            county='Test County',
            original_bag='{}',
            stripe_pid='testpid12345'
        )
        self.assertIsNotNone(order.order_number)

class OrderLineItemModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.product = Product.objects.create(name='Test Product', price=Decimal('10.00'))
        self.order = Order.objects.create(
            user_profile=self.user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            town_or_city='Test City',
            street_address1='123 Test St',
            street_address2='',
            county='Test County',
            original_bag='{}',
            stripe_pid='testpid12345'
        )

    def test_lineitem_total_calculation(self):
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
        )
        line_item.save()
        self.assertEqual(line_item.lineitem_total, self.product.price * 3)

    def test_order_total_updates_with_lineitem(self):
        line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )
        self.order.update_total()
        self.assertEqual(self.order.order_total, self.product.price)

        # Add another line item and check totals again
        line_item2 = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )
        self.order.update_total()
        self.assertEqual(self.order.order_total, self.product.price * 3)
