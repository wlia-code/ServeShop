from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    # Product detail view
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    # Add, edit, and delete products
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path(
        'delete/<int:product_id>/',
        views.delete_product,
        name='delete_product'
    ),
    # wishlist management
    path(
        'product/<int:product_id>/add_to_wishlist/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('wishlist/remove/', views.remove_from_wishlist_ajax, name='remove_from_wishlist_ajax'),
    # Submit testimonials and contact requests
    path(
        'submit_testimonial/',
        views.submit_testimonial,
        name='submit_testimonial'
    ),
    path(
        'submit_contact_request/',
        views.submit_contact_request,
        name='submit_contact_request'
    ),
    # Success page
    path('success/', views.success, name='success_url'),
    path('<int:product_id>/reviews/', views.all_reviews, name='all_reviews'),
]
