from django.test import TestCase
from .models import Category, Product, ProductReview, Wishlist, Testimonial
from django.contrib.auth.models import User

class CategoryModelTest(TestCase):
    def test_string_representation(self):
        category = Category(name='Books')
        self.assertEqual(str(category), category.name)

class ProductModelTest(TestCase):
    def test_string_representation(self):
        category = Category.objects.create(name='Books')
        product = Product(name='Django for Beginners', category=category, price=29.99)
        self.assertEqual(str(product), product.name)

class ProductReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.category = Category.objects.create(name='Books')
        self.product = Product.objects.create(
            name='Test Product', price=10.00, category=self.category
        )

    def test_product_review_creation(self):
        review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='Great product!'
        )
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(str(review), f"Review by {self.user.username}")

class WishlistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')

    def test_wishlist_creation(self):
        wishlist = Wishlist.objects.create(user=self.user)
        self.assertEqual(str(wishlist), f"{self.user.username}'s Wishlist")

class TestimonialModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')

    def test_testimonial_creation(self):
        testimonial = Testimonial.objects.create(
            user=self.user,
            text='Great service!'
        )
        self.assertEqual(str(testimonial), f"Testimonial by {self.user.username}")
