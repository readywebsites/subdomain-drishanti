#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Category, SubCategory, Product

def create_sample_data():
    # Create categories
    gold, _ = Category.objects.get_or_create(name='Gold', defaults={'slug': 'gold'})
    silver, _ = Category.objects.get_or_create(name='Silver', defaults={'slug': 'silver'})
    gifting, _ = Category.objects.get_or_create(name='Gifting', defaults={'slug': 'gifting'})

    # Create subcategories for Gold
    SubCategory.objects.get_or_create(category=gold, name='Stripes Kids Chain', defaults={'slug': 'stripes-kids-chain'})
    SubCategory.objects.get_or_create(category=gold, name='Stripes Diamonds', defaults={'slug': 'stripes-diamonds'})
    SubCategory.objects.get_or_create(category=gold, name='Thread', defaults={'slug': 'thread'})

    # Create subcategories for Silver
    SubCategory.objects.get_or_create(category=silver, name='Plain Kids', defaults={'slug': 'plain-kids'})
    SubCategory.objects.get_or_create(category=silver, name='Stripes Kids', defaults={'slug': 'stripes-kids'})
    SubCategory.objects.get_or_create(category=silver, name='Swastik Kids', defaults={'slug': 'swastik-kids'})

    # Create subcategories for Gifting
    SubCategory.objects.get_or_create(category=gifting, name='Gifts For Her', defaults={'slug': 'gifts-for-her'})
    SubCategory.objects.get_or_create(category=gifting, name='Birthday Gifts', defaults={'slug': 'birthday-gifts'})

    # Create a sample product
    gold_sub = SubCategory.objects.filter(category=gold).first()
    if gold_sub:
        Product.objects.get_or_create(
            name='Luxury Gold Bracelet',
            defaults={
                'slug': 'luxury-gold-bracelet',
                'price': 2500,
                'material': 'Gold',
                'type': 'Stripes',
                'category': 'Kids',
                'new_category': gold,
                'subcategory': gold_sub,
                'description': 'Beautiful gold bracelet for kids',
                'stock': 10,
                'is_bestseller': True,
                'is_featured': True,
                'is_active': True,
                'image': 'products/sample.jpg',  # This will need to be uploaded via admin
                'gallery_images': ['products/gallery1.jpg', 'products/gallery2.jpg']
            }
        )

    print('Sample data created successfully!')

if __name__ == '__main__':
    create_sample_data()