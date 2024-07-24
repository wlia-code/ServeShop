from django.shortcuts import render
from products.models import Testimonial

# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def index(request):
    testimonials = Testimonial.objects.filter(approved=True).order_by('-created_at')[:3]
    return render(request, 'home/index.html', {'testimonials': testimonials})
