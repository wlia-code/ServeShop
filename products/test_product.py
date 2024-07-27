from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, Wishlist, Testimonial

class ProductViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            category=self.category,
            description='A test product'
        )

    def test_all_products_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, self.product.name)

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, self.product.name)

    def test_add_product_view(self):
        user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('add_product'), {
            'name': 'New Product',
            'price': 20.00,
            'category': self.category.id,
            'description': 'A new product',
        })
        self.assertEqual(response.status_code, 302)  # Redirects after adding

    def test_edit_product_view(self):
        user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('edit_product', args=[self.product.id]), {
            'name': 'Updated Product',
            'price': 15.00,
            'category': self.category.id,
            'description': 'An updated product',
        })
        self.assertEqual(response.status_code, 302)  # Redirects after editing
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, 'Updated Product')

    def test_delete_product_view(self):
        user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after deleting
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

class TestimonialModelTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='johndoe', password='password')
        
        # Create a testimonial using the correct fields
        self.testimonial = Testimonial.objects.create(
            user=self.user,  # Set the user field correctly
            text='Great service!',
            rating=5
        )

    def test_testimonial_creation(self):
        # Ensure the testimonial was created correctly
        self.assertEqual(self.testimonial.user.username, 'johndoe')
        self.assertEqual(self.testimonial.text, 'Great service!')
        self.assertEqual(self.testimonial.rating, 5)
