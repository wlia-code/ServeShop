from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),  # Home page
    path(
        'ajax/latest-products/',
        views.ajax_latest_products,
        name='ajax_latest_products'
    ),  # AJAX endpoint for fetching latest products
    path('testimonials/', views.testimonials, name='testimonials'),
]
