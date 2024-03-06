# urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart_view'),
    path('user/', views.user_detail, name='user_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('login_register/', views.login_register, name='login_register'),
    path('login/', views.login_view, name='login_user'),
    path('register/', views.register_view, name='register_user'),
]

