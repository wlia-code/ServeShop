from django.shortcuts import render
from products.models import Testimonial
from products.models import Product
# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')

def index(request):
    # Fetch the latest 100 products for display
    products = Product.objects.all()[:6]
    # Fetch the latest 3 admin approved testimonials
    testimonials = Testimonial.objects.filter(approved=True).order_by('-created_at')[:3]
    return render(request, 'home/index.html', {'products': products, 'testimonials': testimonials})
