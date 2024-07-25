from django.test import TestCase
from .forms import ProductForm, ContactForm, TestimonialForm
from .models import Product, Category

class TestProductForm(TestCase):
    def test_product_form_valid_data(self):
        category = Category.objects.create(name='Books', friendly_name='Books')
        form = ProductForm(data={
            'name': 'Test Product',
            'price': 10.00,
            'category': category.id,
        })
        self.assertTrue(form.is_valid())

    def test_product_form_invalid_data(self):
        form = ProductForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Assuming name and price are required

class TestContactForm(TestCase):
    def test_contact_form_valid_data(self):
        form = ContactForm(data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        })
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_data(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # All fields are required

class TestTestimonialForm(TestCase):
    def test_testimonial_form_valid_data(self):
        form = TestimonialForm(data={
            'text': 'Great service!',
            'review': '5 stars'
        })
        self.assertTrue(form.is_valid())

    def test_testimonial_form_invalid_data(self):
        form = TestimonialForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Text is required
