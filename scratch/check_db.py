import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Category, SubCategory

print("Categories:")
for cat in Category.objects.all():
    print(f"ID: {cat.id}, Name: {cat.name}")
    for sub in cat.subcategories.all():
        print(f"  - Sub ID: {sub.id}, Name: {sub.name}")
