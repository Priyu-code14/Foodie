from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import Food, CartItem, Order, OrderItem


DELIVERY_FEE = Decimal("40.00")


# =========================
# HOME
# =========================

def home(request):
    foods = Food.objects.filter(is_available=True)[:6]

    return render(
        request,
        "home.html",
        {"foods": foods}
    )


# =========================
# MENU
# =========================

def menu(request):
    category = request.GET.get("category", "All")

    foods = Food.objects.filter(is_available=True)

    if category != "All":
        foods = foods.filter(category=category)

    categories = [x[0] for x in Food.CATEGORY_CHOICES]

    return render(
        request,
        "menu.html",
        {
            "foods": foods,
            "categories": categories,
            "selected": category,
        }
    )


# =========================
# REGISTER
# =========================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")

        if not username or not email or not password:
            messages.error(
                request,
                "Please fill all required fields."
            )

        elif password != confirm:
            messages.error(
                request,
                "Passwords do not match."
            )

        elif User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists."
            )

        elif User.objects.filter(email=email).exists():
            messages.error(
                request,
                "Email is already registered."
            )

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect("home")

    return render(
        request,
        "accounts/register.html"
    )


# =========================
# LOGIN
# =========================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            return redirect(
                request.GET.get("next", "home")
            )

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


# =========================
# LOGOUT
# =========================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("home")


# =========================
# ADD TO CART
# =========================

@login_required
def add_to_cart(request, food_id):

    food = get_object_or_404(
        Food,
        id=food_id,
        is_available=True
    )

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        food=food
    )

    if not created:
        item.quantity += 1
        item.save(update_fields=["quantity"])

    messages.success(
        request,
        f"{food.name} added to cart."
    )

    return redirect(
        request.META.get("HTTP_REFERER", "menu")
    )


# =========================
# CART
# =========================

@login_required
def cart(request):

    items = CartItem.objects.filter(
        user=request.user
    ).select_related("food")

    subtotal = sum(
        (item.subtotal for item in items),
        Decimal("0.00")
    )

    delivery = (
        DELIVERY_FEE
        if items
        else Decimal("0.00")
    )

    total = subtotal + delivery

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "subtotal": subtotal,
            "delivery": delivery,
            "total": total,
        }
    )


# =========================
# UPDATE CART
# =========================

@login_required
def update_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    if request.method == "POST":

        try:
            quantity = int(
                request.POST.get("quantity", 1)
            )
        except (TypeError, ValueError):
            quantity = 1

        if quantity > 0:

            item.quantity = min(
                quantity,
                20
            )

            item.save(
                update_fields=["quantity"]
            )

        else:
            item.delete()

    return redirect("cart")


# =========================
# REMOVE FROM CART
# =========================

@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )

    item.delete()

    messages.info(
        request,
        "Item removed from cart."
    )

    return redirect("cart")


# =========================
# CHECKOUT
# =========================

@login_required
def checkout(request):

    items = CartItem.objects.filter(
        user=request.user
    ).select_related("food")

    if not items.exists():

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("menu")

    subtotal = sum(
        (item.subtotal for item in items),
        Decimal("0.00")
    )

    delivery = DELIVERY_FEE
    total = subtotal + delivery

    if request.method == "POST":

        address = request.POST.get(
            "address",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        payment_method = request.POST.get(
            "payment_method",
            "COD"
        )

        if not address or not phone:

            messages.error(
                request,
                "Please enter your delivery address and phone number."
            )

        else:

            with transaction.atomic():

                order = Order.objects.create(
                    user=request.user,
                    total_amount=total,
                    delivery_address=address,
                    phone=phone,
                    payment_method=payment_method,
                )

                for item in items:

                    OrderItem.objects.create(
                        order=order,
                        food=item.food,
                        quantity=item.quantity,
                        price=item.food.price
                    )

                if payment_method == "COD":

                    order.payment_status = "Pending"

                    order.save(
                        update_fields=["payment_status"]
                    )

                    items.delete()

                    return redirect(
                        "order_success",
                        order_id=order.id
                    )

            return redirect(
                "payment",
                order_id=order.id
            )

    return render(
        request,
        "checkout.html",
        {
            "items": items,
            "subtotal": subtotal,
            "delivery": delivery,
            "total": total,
        }
    )


# =========================
# PAYMENT
# =========================

@login_required
def payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.payment_status == "Paid":

        return redirect(
            "order_success",
            order_id=order.id
        )

    if request.method == "POST":

        # Demo payment only.
        # No card/UPI information is stored.

        order.payment_status = "Paid"
        order.status = "Confirmed"

        order.save(
            update_fields=[
                "payment_status",
                "status"
            ]
        )

        CartItem.objects.filter(
            user=request.user
        ).delete()

        messages.success(
            request,
            "Payment successful!"
        )

        return redirect(
            "order_success",
            order_id=order.id
        )

    return render(
        request,
        "payment.html",
        {"order": order}
    )


# =========================
# ORDER SUCCESS
# =========================

@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "order_success.html",
        {"order": order}
    )


# =========================
# MY ORDERS
# =========================

@login_required
def orders(request):

    user_orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items__food")
    )

    return render(
        request,
        "orders.html",
        {"orders": user_orders}
    )