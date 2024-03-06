# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Product, Cart, CartItem, Address

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shopee/product_list.html', {'products': products})

def cart_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []
    return render(request, 'shopee/cart.html', {'cart_items': cart_items})

def user_detail(request):
    user = request.user
    address = Address.objects.filter(user=user).first()
    return render(request, 'shopee/user_detail.html', {'user': user, 'address': address})

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, 'Product added to cart successfully.')
    return redirect('product_list')

def update_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity', 0))
        cart_item = CartItem.objects.get(id=cart_item_id)
        if quantity == 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
    return redirect('cart_view')

def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('product_list')
                else:
                    messages.error(request, 'Invalid username or password.')
        elif 'register' in request.POST:
            registration_form = UserCreationForm(request.POST)
            if registration_form.is_valid():
                registration_form.save()
                # Auto-login after register or redirect to a login page
                return redirect('login_user')  # Adjust the redirect as necessary
    else:
        login_form = AuthenticationForm()
        registration_form = UserCreationForm()

    return render(request, 'shopee/login_register.html', {'login_form': login_form, 'registration_form': registration_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')  # Redirect to a desired page
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'shopee/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('login_user')  # Redirect to the login page
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'shopee/register.html', {'form': form})