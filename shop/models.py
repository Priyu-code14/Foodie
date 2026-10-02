from django.conf import settings
from django.db import models

class Food(models.Model):
    CATEGORY_CHOICES = [
        ("Pizza", "Pizza"),
        ("Burgers", "Burgers"),
        ("Chinese", "Chinese"),
        ("Drinks", "Drinks"),
    ]
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "food"], name="unique_user_food_cart")
        ]

    @property
    def subtotal(self):
        return self.food.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Preparing", "Preparing"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    PAYMENT_CHOICES = [("COD", "Cash on Delivery"), ("UPI", "UPI"), ("CARD", "Card")]
    PAYMENT_STATUS_CHOICES = [("Pending", "Pending"), ("Paid", "Paid")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="COD")
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"ORD{self.id:04d}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity
