#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.files import File
from api.models import Category, SubCategory, Product, HomepageSlider

def create_homepage_slides():
    """
    Populates the HomepageSlider model with data from the frontend.
    """
    # Clean up existing slides to avoid duplicates on reruns
    HomepageSlider.objects.all().delete()
    print('Existing homepage slides cleared.')

    slides_data = [
        {
            'title': 'Homepage Banner 1',
            'image_path': '../drishanti-v2/public/images/banner1.webp',
            'text': 'Rakshapotlis\nReimagined.',
            'description': 'GOLD | SILVER | DIAMONDS',
            'button_1_text': 'What is Rakshapotli',
            'button_1_link': '/what-is-rakshapotli',
            'button_2_text': 'Discover Our Story',
            'button_2_link': '/about',
            'display_order': 0,
        },
        {
            'title': 'Homepage Banner 2',
            'image_path': '../drishanti-v2/public/images/banner2.webp',
            'text': 'Rakshapotlis\nReimagined.',
            'description': 'GOLD | SILVER | DIAMONDS',
            'button_1_text': 'What is Rakshapotli',
            'button_1_link': '/what-is-rakshapotli',
            'button_2_text': 'Discover Our Story',
            'button_2_link': '/about',
            'display_order': 1,
        },
        {
            'title': 'Homepage Banner 3 (Baby)',
            'image_path': '../drishanti-v2/public/images/baby-banner.webp',
            'text': 'Rakshapotlis\nReimagined.',
            'description': 'GOLD | SILVER | DIAMONDS',
            'button_1_text': 'What is Rakshapotli',
            'button_1_link': '/what-is-rakshapotli',
            'button_2_text': 'Discover Our Story',
            'button_2_link': '/about',
            'display_order': 2,
        }
    ]

    for index, data in enumerate(slides_data):
        # Construct the full path to the image
        image_path = os.path.join(os.path.dirname(__file__), data['image_path'])

        if not os.path.exists(image_path):
            print(f"Warning: Image not found at {image_path}. Skipping slide.")
            continue

        # Create the slide instance without the image first
        slide, created = HomepageSlider.objects.get_or_create(
            title=data['title'],
            display_order=data['display_order'],
            defaults={
                'text': data['text'].replace('\\n', '\n'),
                'text_color': '#FFFFFF',
                'text_alignment': 'left',
                'button_1_text': data['button_1_text'],
                'button_1_link': data['button_1_link'],
                'button_1_color': '#b39168',
                'button_2_text': data['button_2_text'],
                'button_2_link': data['button_2_link'],
                'button_2_color': '#FFFFFF',
                'is_active': True,
            }
        )

        if created:
            # Now, attach the image
            with open(image_path, 'rb') as f:
                # We use the name of the file for the image field
                image_name = os.path.basename(image_path)
                slide.slider_image.save(image_name, File(f), save=True)
            print(f"Created slide: '{data['title']}' and uploaded image.")
        else:
            print(f"Slide '{data['title']}' already exists. Skipping creation.")


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
                'image': 'products/sample.webp',  # This will need to be uploaded via admin
                'gallery_images': ['products/gallery1.webp', 'products/gallery2.webp']
            }
        )

    print('Sample data created successfully!')

if __name__ == '__main__':
    # You can choose what to run here
    # create_sample_data()
    create_homepage_slides()
