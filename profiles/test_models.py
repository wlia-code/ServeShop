from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, ProductReview
from products.models import Product

class UserProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.get(user=self.user)

    def test_user_profile_creation(self):
        self.assertIsInstance(self.user_profile, UserProfile)
        self.assertEqual(self.user_profile.user, self.user)

    def test_user_profile_string_representation(self):
        self.assertEqual(str(self.user_profile), self.user.username)

    def test_default_fields_blank(self):
        self.assertIsNone(self.user_profile.default_phone_number)
        self.assertIsNone(self.user_profile.default_street_address1)
        self.assertIsNone(self.user_profile.default_street_address2)
        self.assertIsNone(self.user_profile.default_town_or_city)
        self.assertIsNone(self.user_profile.default_county)
        self.assertIsNone(self.user_profile.default_postcode)
        self.assertIsNone(self.user_profile.default_country.code)

class ProductReviewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name='Test Product', price=100)
        self.review = ProductReview.objects.create(
            product=self.product,
            customer_name='John Doe',
            rating=5,
            comment='Great product!',
            approved=True
        )

    def test_product_review_creation(self):
        self.assertIsInstance(self.review, ProductReview)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.customer_name, 'John Doe')
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Great product!')
        self.assertTrue(self.review.approved)

    def test_product_review_string_representation(self):
        expected_str = f"Review by John Doe for {self.product.name}"
        self.assertEqual(str(self.review), expected_str)
