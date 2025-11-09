from django.contrib import admin
from .models import Product, Cart, Wishlist, Order, OrderItem


# 🛍️ Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price', 'featured')
    list_filter = ('category', 'subcategory', 'featured')
    search_fields = ('name', 'description')


# 🛒 Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__name')


# 💖 Wishlist Admin
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__name')


# 🧾 OrderItem Inline (for viewing items under each Order)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# 💳 Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_method', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'name', 'email')
    inlines = [OrderItemInline]


# 🧾 OrderItem Admin (optional, to view all items separately)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__user__username', 'product__name')
