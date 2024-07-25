from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
import random
from products.models import Product, Testimonial
# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')

def ajax_latest_products(request):
    product_ids = Product.objects.values_list('id', flat=True)  # Get all product IDs
    random_ids = random.sample(list(product_ids), min(len(product_ids), 3))  # Pick random IDs
    products = Product.objects.filter(id__in=random_ids)
    products_data = [model_to_dict(product, fields=['id', 'name', 'price', 'image']) for product in products]
    for product in products_data:
        product['image'] = request.build_absolute_uri(product['image'].url) if 'image' in product and product['image'] else None
    return JsonResponse({'products': products_data})


def index(request):
    # Fetch the latest three approved testimonials for the home page
    testimonials = Testimonial.objects.filter(approved=True).order_by('-created_at')[:3]
    # Add star range information to each testimonial
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
    return render(request, 'home/index.html', {
        'testimonials': testimonials_data,
    })

def testimonials(request):
    # Fetch all approved testimonials
    testimonials = Testimonial.objects.filter(approved=True).order_by('-created_at')
    # Add star range information to each testimonial
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
    return render(request, 'home/testimonials.html', {'testimonials': testimonials_data})