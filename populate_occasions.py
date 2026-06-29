

import os
import sys
import django
import shutil

# --- SETUP DJANGO ENVIRONMENT ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(script_dir)
sys.path.append(project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# --- IMPORT YOUR MODELS ---
from api.models import OccasionsSection, OccasionCard

# --- DEFINE STATIC DATA ---
header_data = {
    "title": "Find the Perfect Rakshapotli for Every Occasion",
    "subtitle": "Thoughtfully curated gifts for life's beautiful moments."
}

cards_data = [
    {"title": "Newborns and Infants", "icon_name": "Baby", "image_name": "newborn.webp", "link": "#"},
    {"title": "Moms and Expectant Mothers", "icon_name": "Heart", "image_name": "moms.webp", "link": "#"},
    {"title": "Paarnas", "icon_name": "Sun", "image_name": "paarnas.webp", "link": "#"},
    {"title": "Tapasvis (Ascetics)", "icon_name": "Flower2", "image_name": "tapasvi.webp", "link": "#"},
    {"title": "Prabhavna", "icon_name": "Stars", "image_name": "prabhavna.webp", "link": "#"},
    {"title": "Housewarming and Gifting", "icon_name": "Home", "image_name": "housewarming.webp", "link": "#"},
    {"title": "Puja Return Gifts", "icon_name": "Gift", "image_name": "Puja-gifts.webp", "link": "#"},
    {"title": "Wedding and Engagement", "icon_name": "Crown", "image_name": "wedding.webp", "link": "#"},
    {"title": "Festivals", "icon_name": "Stars", "image_name": "festivals.webp", "link": "#"},
    {"title": "Spiritual Retreats", "icon_name": "Church", "image_name": "spiritual.webp", "link": "#"},
    {"title": "Birthdays and Milestones", "icon_name": "Award", "image_name": "birthday.webp", "link": "#"},
    {"title": "Personal Protection and Devotion", "icon_name": "ShieldCheck", "image_name": "personal-protection.webp", "link": "#"},
    {"title": "Rakshabandhan", "icon_name": "ShieldCheck", "image_name": "rakshabandhan.webp", "link": "#"},
    {"title": "Poojans", "icon_name": "Sparkles", "image_name": "poojan.webp", "link": "#"},
]

# --- DEFINE FILE PATHS ---
frontend_images_dir = os.path.join(project_dir, 'dist', 'images')
django_media_dir = os.path.abspath(os.path.join(project_dir, 'media', 'occasions'))

# --- MAIN POPULATION LOGIC ---
def populate_occasions():
    print("Starting Occasions section population...")
    os.makedirs(django_media_dir, exist_ok=True)
    
    # --- Clear old data ---
    OccasionsSection.objects.all().delete()
    OccasionCard.objects.all().delete()
    print("Cleared existing Occasions Section and Cards.")

    # --- Populate Header Section ---
    section, created = OccasionsSection.objects.get_or_create(id=1, defaults=header_data)
    if created:
        print("-> Successfully CREATED section header.")
    else:
        print("-> Successfully UPDATED section header.")

    # --- Populate Cards for the Section ---
    for index, card_data in enumerate(cards_data):
        print(f"Processing occasion card: {card_data['title']}")

        # --- Image Handling ---
        source_image_path = os.path.join(frontend_images_dir, card_data['image_name'])
        destination_image_path = os.path.join(django_media_dir, card_data['image_name'])
        
        if not os.path.exists(source_image_path):
            print(f"  [!] WARNING: Source image not found at {source_image_path}. Skipping.")
            continue

        try:
            shutil.copy2(source_image_path, destination_image_path)
            print(f"  -> Copied image to {destination_image_path}")
        except Exception as e:
            print(f"  [!] ERROR: Could not copy image. {e}. Skipping.")
            continue
            
        django_image_path = os.path.join('occasions', card_data['image_name'])

        # --- Create Card Instance ---
        try:
            card, created = OccasionCard.objects.update_or_create(
                section=section,
                title=card_data['title'],
                defaults={
                    'icon_name': card_data['icon_name'],
                    'hover_image': django_image_path,
                    'link': card_data['link'],
                    'display_order': index,
                    'is_active': True,
                }
            )
            if created:
                print(f"  -> Successfully CREATED card: {card.title}")
            else:
                print(f"  -> Successfully UPDATED card: {card.title}")

        except Exception as e:
            print(f"  [!] ERROR: Could not create card object in database. {e}")

    print("\nPopulation script finished.")

if __name__ == '__main__':
    populate_occasions()
