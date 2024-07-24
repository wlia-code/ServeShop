from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('product/<int:product_id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('submit_testimonial/', views.submit_testimonial, name='submit_testimonial'),
    path('submit_contact_request/', views.submit_contact_request, name='submit_contact_request'),
    path('success/', views.success, name='success_url'),
]