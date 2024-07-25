from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, ProductReview, Wishlist, Testimonial
from .forms import ProductForm, ContactForm, TestimonialForm

class ProductViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.superuser = User.objects.create_superuser(username='admin', password='12345')
        self.category = Category.objects.create(name='Books', friendly_name='Books')
        self.product = Product.objects.create(
            name='Test Product', price=10.00, category=self.category
        )

    def test_all_products_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_add_product_view(self):
        self.client.login(username='admin', password='12345')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    def test_edit_product_view(self):
        self.client.login(username='admin', password='12345')
        response = self.client.get(reverse('edit_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/edit_product.html')

    def test_delete_product_view(self):
        self.client.login(username='admin', password='12345')
        response = self.client.post(reverse('delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after deletion
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_add_review_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_review', args=[self.product.id]), {
            'rating': 5, 'comment': 'Great product!'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to product detail
        self.assertTrue(ProductReview.objects.filter(product=self.product).exists())

    def test_add_to_wishlist_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('add_to_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to wishlist
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertIn(self.product, wishlist.products.all())

    def test_view_wishlist(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/wishlist.html')

    def test_submit_testimonial_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('submit_testimonial'), {
            'text': 'Great service!', 'review': '5 stars'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home
        self.assertTrue(Testimonial.objects.filter(user=self.user).exists())

    def test_submit_contact_request_view(self):
        response = self.client.post(reverse('submit_contact_request'), {
            'name': 'Test User', 'email': 'test@example.com',
            'subject': 'Test Subject', 'message': 'Test Message'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to success
        # Assuming email sending is mocked in the test environment

    def test_success_view(self):
        response = self.client.get(reverse('success_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/success.html')
