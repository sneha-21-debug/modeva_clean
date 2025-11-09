from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ----------------------------------------------------
# 🛍️ Product Model
# ----------------------------------------------------
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('accessories', 'Accessories'),
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
    ]
    SUBCATEGORY_CHOICES = [
        ('handbags', 'Handbags'), ('sunglasses', 'Sunglasses'), ('watches', 'Watches'),
        ('jewellery', 'Jewellery'), ('men_shirts', 'Men Shirts'), ('men_jeans', 'Men Jeans'),
        ('men_jackets', 'Men Jackets'), ('men_shoes', 'Men Shoes'),
        ('women_dresses', 'Women Dresses'), ('women_tops', 'Women Tops'),
        ('women_jeans', 'Women Jeans'), ('women_sarees', 'Women Sarees'),
        ('kids_tshirts', 'Kids T-Shirts'), ('kids_pants', 'Kids Pants'),
        ('kids_shoes', 'Kids Shoes'), ('kids_toys', 'Kids Toys'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ----------------------------------------------------
# 🛒 Cart Model
# ----------------------------------------------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    def get_total(self):
        return self.product.price * self.quantity


# ----------------------------------------------------
# 💖 Wishlist Model
# ----------------------------------------------------
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ♥ {self.product.name}"


# ----------------------------------------------------
# 📦 Order Model
# ----------------------------------------------------
class Order(models.Model):
    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


# ----------------------------------------------------
# 🧾 OrderItem Model (Each product inside an order)
# ----------------------------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total(self):
        return self.quantity * self.price
