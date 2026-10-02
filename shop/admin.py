from django.contrib import admin
from .models import Food, CartItem, Order, OrderItem

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "food", "quantity")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("food", "quantity", "price")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "total_amount", "status", "payment_method", "payment_status", "created_at")
    list_filter = ("status", "payment_status", "payment_method")
    search_fields = ("user__username", "phone", "delivery_address")
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "food", "quantity", "price")
