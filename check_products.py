import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Product

print("--- All Active Product Slugs ---")
active_products = Product.objects.filter(is_active=True)
if active_products.exists():
    for p in active_products:
        print(p.slug)
else:
    print("No active products found.")
print("--------------------------------")

specific_slug = 'sacred-plain-rakshapotli'
product = Product.objects.filter(slug=specific_slug, is_active=True).first()
if product:
    print(f"Specific Product Found: {product.name}, Slug: {product.slug}, Active: {product.is_active}")
else:
    print(f"Specific Product '{specific_slug}' not found or not active.")
