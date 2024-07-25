from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
]