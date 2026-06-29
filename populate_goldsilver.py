
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

# --- IMPORT YOUR MODEL ---
from api.models import GoldSilverSection

# --- DEFINE STATIC DATA FROM GoldSilver.jsx ---
goldsilver_data = [
    {
        'section_type': 'gold',
        'title': 'Gold Collection',
        'subtitle': 'Rakshapotli crafted in',
        'description': '18kt Hallmarked Gold',
        'image_name': 'gold.webp',
        'button_text': 'EXPLORE',
        'button_link': '/shop/gold',
        'title_color': '#64490f',
        'line_color': '#664d14',
        'collection_color': '#272114',
        'text_color': '#68490c',
        'button_bg_color': '#644b15',
        'object_position': 'object-center',
        'display_order': 0,
        'title_suffix': 'Collection',
    },
    {
        'section_type': 'silver',
        'title': 'Silver Collection',
        'subtitle': 'Rakshapotli crafted in',
        'description': '925 Hallmarked Silver',
        'image_name': 'silver1.webp',
        'button_text': 'EXPLORE',
        'button_link': '/shop/silver',
        'title_color': '#252525',
        'line_color': '#65696d',
        'collection_color': '#ffffff',
        'text_color': '#404040',
        'button_bg_color': '#252525',
        'object_position': 'object-bottom',
        'display_order': 1,
        'title_suffix': 'Collection',
    },
]

# --- DEFINE FILE PATHS ---
frontend_images_dir = os.path.abspath(os.path.join(project_dir, '..', 'drishanti-v2', 'public', 'images'))
django_media_dir = os.path.abspath(os.path.join(project_dir, 'media', 'goldsilver'))

# --- MAIN POPULATION LOGIC ---
def populate_goldsilver():
    print("Starting Gold/Silver section population...")
    os.makedirs(django_media_dir, exist_ok=True)
    
    GoldSilverSection.objects.all().delete()
    print("Cleared existing Gold/Silver Section entries.")

    for item_data in goldsilver_data:
        print(f"Processing section: {item_data['title']}")

        # --- Image Handling ---
        source_image_path = os.path.join(frontend_images_dir, item_data['image_name'])
        destination_image_path = os.path.join(django_media_dir, item_data['image_name'])
        
        if not os.path.exists(source_image_path):
            print(f"  [!] WARNING: Source image not found at {source_image_path}. Skipping.")
            continue

        try:
            shutil.copy2(source_image_path, destination_image_path)
            print(f"  -> Copied image to {destination_image_path}")
        except Exception as e:
            print(f"  [!] ERROR: Could not copy image. {e}. Skipping.")
            continue
            
        django_image_path = os.path.join('goldsilver', item_data['image_name'])

        # --- Create Model Instance ---
        try:
            section, created = GoldSilverSection.objects.update_or_create(
                section_type=item_data['section_type'],
                defaults={
                    'title': item_data['title'],
                    'subtitle': item_data['subtitle'],
                    'description': item_data['description'],
                    'image': django_image_path,
                    'button_text': item_data['button_text'],
                    'button_link': item_data['button_link'],
                    'title_color': item_data['title_color'],
                    'collection_color': item_data['collection_color'],
                    'text_color': item_data['text_color'],
                    'line_color': item_data['line_color'],
                    'button_bg_color': item_data['button_bg_color'],
                    'object_position': item_data['object_position'],
                    'display_order': item_data['display_order'],
                    'is_active': True,
                }
            )
            if created:
                print(f"  -> Successfully CREATED section: {section.title}")
            else:
                print(f"  -> Successfully UPDATED section: {section.title}")

        except Exception as e:
            print(f"  [!] ERROR: Could not create section object in database. {e}")

    print("\nPopulation script finished.")

if __name__ == '__main__':
    populate_goldsilver()
