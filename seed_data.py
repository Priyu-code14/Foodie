import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from shop.models import Food

foods = [
    ("Margherita Pizza", "Pizza", "Classic pizza with tomato, mozzarella and herbs.", "199.00", "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=900"),
    ("Veggie Pizza", "Pizza", "Loaded with fresh vegetables and mozzarella.", "249.00", "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=900"),
    ("Cheese Burger", "Burgers", "Crispy veg patty, cheese, lettuce and sauce.", "159.00", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=900"),
    ("Paneer Burger", "Burgers", "Spicy paneer patty with fresh veggies.", "179.00", "https://images.unsplash.com/photo-1550547660-d9450f859349?w=900"),
    ("Veg Noodles", "Chinese", "Stir-fried noodles with colourful vegetables.", "149.00", "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=900"),
    ("Fried Rice", "Chinese", "Aromatic fried rice with vegetables.", "159.00", "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=900"),
    ("Coke", "Drinks", "Chilled soft drink.", "50.00", "https://images.unsplash.com/photo-1629203849820-fdd70d49c38e?w=900"),
    ("Cold Coffee", "Drinks", "Creamy chilled coffee.", "90.00", "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=900"),
]
for name, category, desc, price, image in foods:
    Food.objects.get_or_create(name=name, defaults={"category":category,"description":desc,"price":price,"image":image})
print(f"Seeded {Food.objects.count()} foods.")
