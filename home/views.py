import random
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from products.models import Testimonial, Product
# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')

def ajax_latest_products(request):
    product_ids = Product.objects.values_list('id', flat=True)  # Get all product IDs
    random_ids = random.sample(list(product_ids), min(len(product_ids), 6))  # Pick 6 random IDs
    products = Product.objects.filter(id__in=random_ids)
    products_data = [model_to_dict(product, fields=['id', 'name', 'price', 'image']) for product in products]
    for product in products_data:
        product['image'] = request.build_absolute_uri(product['image'].url) if 'image' in product and product['image'] else None
    return JsonResponse({'products': products_data})
