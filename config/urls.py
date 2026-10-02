from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/<int:order_id>/", views.payment, name="payment"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    path("orders/", views.orders, name="orders"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
