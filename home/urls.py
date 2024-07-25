from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('ajax/latest-products/', views.ajax_latest_products, name='ajax_latest_products'),  # AJAX endpoint
    path('testimonials/', views.testimonials, name='testimonials'),
]
