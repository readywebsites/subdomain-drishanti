
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
from api.models import ComponentsSection, ComponentCard

# --- DEFINE STATIC DATA ---
header_data = {
    "title": "THE ANATOMY OF SACRED CRAFT",
    "subtitle_part_1": "Components of",
    "subtitle_part_2": "Rakshapotli",
}

cards_data = [
  {
    "display_id": "01",
    "image_name": "Gold  Silver Structure.webp",
    "icon_name": "Gem",
    "title": "Gold / Silver Structure",
    "description": "Crafted in premium 18k gold plating or sterling silver for lasting purity.",
  },
  {
    "display_id": "02",
    "image_name": "vasakshep.webp",
    "icon_name": "Sparkles",
    "title": "Encapsulated Vasakshep",
    "description": "Sacred, consecrated Vedic powders safely housed inside every potli.",
  },
  {
    "display_id": "03",
    "image_name": "enamel.webp",
    "icon_name": "ShieldCheck",
    "title": "German Ceramic",
    "description": "High-durability ceramic coating preserving the sacred hue.",
  },
  {
    "display_id": "04",
    "image_name": "certificate.webp",
    "icon_name": "BadgeCheck",
    "title": "Authentication Certificate",
    "description": "Every piece includes an official hallmark authenticity certificate.",
  },
  {
    "display_id": "05",
    "image_name": "stamping.webp",
    "icon_name": "Fingerprint",
    "title": "Brand Stamping",
    "description": "The DRISHANTI hallmark engraved as a vow of craftsmanship.",
  },
  {
    "display_id": "06",
    "image_name": "comfort-fit.webp",
    "icon_name": "CircleEllipsis",
    "title": "Comfort Fit Construction",
    "description": "Designed ergonomically for a seamless second-skin wearing feel.",
  },
]

# --- DEFINE FILE PATHS ---
frontend_images_dir = os.path.join(project_dir, 'dist', 'images')
django_media_dir = os.path.abspath(os.path.join(project_dir, 'media', 'rakshapotli_components'))

# --- MAIN POPULATION LOGIC ---
def populate_components():
    print("Starting Components of Rakshapotli section population...")
    os.makedirs(django_media_dir, exist_ok=True)
    
    # --- Clear old data ---
    ComponentsSection.objects.all().delete()
    ComponentCard.objects.all().delete()
    print("Cleared existing Components Section and Cards.")

    # --- Populate Header Section ---
    section, created = ComponentsSection.objects.get_or_create(id=1, defaults=header_data)
    if created:
        print("-> Successfully CREATED section header.")
    else:
        print("-> Successfully UPDATED section header.")

    # --- Populate Cards for the Section ---
    for index, card_data in enumerate(cards_data):
        print(f"Processing component card: {card_data['title']}")

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
            
        django_image_path = os.path.join('rakshapotli_components', card_data['image_name'])

        # --- Create Card Instance ---
        try:
            card, created = ComponentCard.objects.update_or_create(
                section=section,
                display_id=card_data['display_id'],
                defaults={
                    'title': card_data['title'],
                    'description': card_data['description'],
                    'image': django_image_path,
                    'icon_name': card_data['icon_name'],
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
    populate_components()
