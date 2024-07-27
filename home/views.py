from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
import random
from products.models import Product, Testimonial

"""
The project structure and some of the
backend code were adapted from the Code Institute's
"Boutique Ado" walk-through project.
(https://codeinstitute.net)
"""


def ajax_latest_products(request):
    """
    A view to provide the latest products data via AJAX.
    Returns a JSON response containing product details.
    """
    product_ids = Product.objects.values_list('id', flat=True)
    random_ids = random.sample(
        list(product_ids), min(len(product_ids), 3)
    )  # Pick random product IDs
    products = Product.objects.filter(id__in=random_ids)
    products_data = [
        model_to_dict(product, fields=['id', 'name', 'price', 'image'])
        for product in products
    ]
    for product in products_data:
        if 'image' in product and product['image']:
            product['image'] = request.build_absolute_uri(product['image'].url)
        else:
            product['image'] = None
    return JsonResponse({'products': products_data})


def index(request):
    """
    A view to return the index page with the latest testimonials.
    Fetches the latest three approved testimonials for display.
    """
    testimonials = Testimonial.objects.filter(
        approved=True
    ).order_by('-created_at')[:3]
    testimonials_data = []
    for testimonial in testimonials:
        testimonials_data.append({
            'username': testimonial.user.username,
            'text': testimonial.text,
            'review': testimonial.review,
            'rating': testimonial.rating,
            'image': testimonial.image.url if testimonial.image else None,
            'star_range': range(testimonial.rating),
            'empty_star_range': range(5 - testimonial.rating),
        })
    return render(request, 'home/index.html', {'testimonials': testimonials_data})  # noqa


def testimonials(request):
    """
    A view to display all approved testimonials.
    """
    testimonials = Testimonial.objects.filter(approved=True).order_by('-created_at')  # noqa
    testimonials_data = []
    for testimonial in testimonials:
        testimonials_data.append({
            'username': testimonial.user.username,
            'text': testimonial.text,
            'review': testimonial.review,
            'rating': testimonial.rating,
            'image': testimonial.image.url if testimonial.image else None,
            'star_range': range(testimonial.rating),
            'empty_star_range': range(5 - testimonial.rating),
        })
    return render(request, 'home/testimonials.html', {'testimonials': testimonials_data})  # noqa
