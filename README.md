# Foodie — Online Food Ordering System

A compact Swiggy/Zomato-style food ordering full-stack project built with Python, Django, MySQL, HTML, CSS, Bootstrap and JavaScript.

## Features
- User registration/login/logout
- Responsive home page
- Food menu with categories
- MySQL-backed food catalogue
- Add/update/remove cart items
- Checkout and delivery details
- Demo COD/UPI/Card payment flow
- Order success page
- My Orders
- Django Admin for food and order management
- Responsive mobile layout

## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a MySQL database named `foodie`.

Configure environment variables or edit `config/settings.py` for local MySQL credentials.

```powershell
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py seed_data.py
py manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

> Payment is intentionally simulated for portfolio/demo use. No real payment is processed.
