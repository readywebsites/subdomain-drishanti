import os
import django
from django.test import RequestFactory
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Product
from api.admin import ProductAdmin
from django.contrib import admin

# Create request
factory = RequestFactory()
request = factory.get('/admin/api/product/add/')

# Get superuser
superuser = User.objects.filter(is_superuser=True).first()
if not superuser:
    # Use any user or create a temporary one
    superuser = User(username='temp_admin', is_staff=True, is_superuser=True)
request.user = superuser

# Get admin instance
product_admin = ProductAdmin(Product, admin.site)

# Render add view
try:
    response = product_admin.add_view(request)
    # Some Django responses don't need explicit render if they are TemplateResponse
    if hasattr(response, 'render'):
        response.render()
    html = response.content.decode('utf-8')
    
    print("--- Rendered Script Tags containing 'chained' ---")
    for line in html.split('\n'):
        if 'chained' in line:
            print(line.strip())
    print("-------------------------------------------------")
except Exception as e:
    print("Error rendering admin view:", str(e))
