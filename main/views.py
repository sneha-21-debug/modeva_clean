from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, Wishlist, Order


# -----------------------
# 🔐 AUTH VIEWS
# -----------------------

def signup_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "❌ Passwords do not match!")
            return redirect('signup_page')

        if User.objects.filter(username=username).exists():
            messages.error(request, "⚠️ Username already taken!")
            return redirect('signup_page')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "✅ Account created successfully! Please log in.")
        return redirect('login_page')

    return render(request, 'signup.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"👋 Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "❌ Invalid username or password.")
            return redirect('login_page')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.info(request, "👋 Logged out successfully.")
    return redirect('home')


# -----------------------
# 🏠 HOME PAGE
# -----------------------

def home(request):
    featured_products = Product.objects.filter(featured=True)
    return render(request, 'home.html', {'featured_products': featured_products})


# -----------------------
# 🛍️ CATEGORY PAGES
# -----------------------

SUBCATEGORIES = {
    'men': ['men_shirts', 'men_jeans', 'men_jackets', 'men_shoes'],
    'women': ['women_dresses', 'women_tops', 'women_jeans', 'women_sarees'],
    'kids': ['kids_tshirts', 'kids_pants', 'kids_shoes', 'kids_toys'],
    'accessories': ['handbags', 'sunglasses', 'watches', 'jewellery'],
}

def accessories(request):
    products = Product.objects.filter(category='accessories')
    return render(request, 'accessories.html', {'products': products})

def men(request):
    products = Product.objects.filter(category='men')
    return render(request, 'men.html', {'products': products})

def women(request):
    products = Product.objects.filter(category='women')
    return render(request, 'women.html', {'products': products})

def kids(request):
    products = Product.objects.filter(category='kids')
    return render(request, 'kids.html', {'products': products})

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})


# -----------------------
# 🧩 SUBCATEGORY PAGE
# -----------------------

def products_by_subcategory(request, subcategory_name):
    """Show all products under a specific subcategory (like men_shirts, women_dresses, etc.)."""
    products = Product.objects.filter(subcategory=subcategory_name)
    return render(request, 'subcategory.html', {
        'products': products,
        'subcategory_name': subcategory_name
    })


# -----------------------
# 🛒 CART FUNCTIONS
# -----------------------

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def remove_from_cart(request, product_id):
    item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    item.delete()
    return redirect('view_cart')


@login_required
def increase_quantity(request, product_id):
    item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    item.quantity += 1
    item.save()
    return redirect('view_cart')


@login_required
def decrease_quantity(request, product_id):
    item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('view_cart')


# -----------------------
# 💖 WISHLIST
# -----------------------

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('view_wishlist')


@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def remove_from_wishlist(request, product_id):
    item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    item.delete()
    return redirect('view_wishlist')


# -----------------------
# 💳 CHECKOUT & ORDERS
# -----------------------

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment_method,
            payment_status='Pending',
            total_amount=total
        )

        if payment_method == "Online":
            return redirect('fake_payment')

        cart_items.delete()
        return redirect('order_success')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})
@login_required
def fake_payment(request):
    """Simulate an online payment step."""
    if request.method == "POST":
        otp = request.POST.get("otp")

        # Simple authentication simulation
        if otp == "1234":  # you can set any OTP for demo
            last_order = Order.objects.filter(user=request.user).last()
            if last_order:
                last_order.payment_status = "Paid"
                last_order.save()
            Cart.objects.filter(user=request.user).delete()
            return redirect('order_success')
        else:
            return render(request, 'fake_payment.html', {"error": "Invalid OTP. Try again."})

    return render(request, 'fake_payment.html')



@login_required
def payment_success(request):
    last_order = Order.objects.filter(user=request.user).last()
    if last_order:
        last_order.payment_status = "Paid"
        last_order.save()
    Cart.objects.filter(user=request.user).delete()
    return redirect('order_success')


@login_required
def order_success(request):
    return render(request, 'order_success.html')


# -----------------------
# 🧾 MY ORDERS PAGE
# -----------------------

@login_required
def my_orders(request):
    """Display all orders placed by the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})
