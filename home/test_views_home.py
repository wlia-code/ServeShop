from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Testimonial
from django.http import JsonResponse

class HomeViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product1 = Product.objects.create(name='Product 1', price=100)
        self.product2 = Product.objects.create(name='Product 2', price=200)
        self.product3 = Product.objects.create(name='Product 3', price=300)
        self.testimonial1 = Testimonial.objects.create(
            user=self.user,
            text='Great product!',
            review='Loved it.',
            rating=5,
            approved=True
        )
        self.testimonial2 = Testimonial.objects.create(
            user=self.user,
            text='Not bad.',
            review='It was okay.',
            rating=3,
            approved=True
        )
        self.testimonial3 = Testimonial.objects.create(
            user=self.user,
            text='Could be better.',
            review='Expected more.',
            rating=2,
            approved=True
        )

    def test_ajax_latest_products_view(self):
        response = self.client.get(reverse('ajax_latest_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response, JsonResponse))
        data = response.json()
        self.assertIn('products', data)
        self.assertTrue(len(data['products']) <= 3)


    def test_testimonials_view(self):
        response = self.client.get(reverse('testimonials'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/testimonials.html')
        self.assertContains(response, self.testimonial2.text)
        self.assertContains(response, self.testimonial3.text)
