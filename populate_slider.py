import os
import sys
import django
import shutil
from django.core.files.images import ImageFile

# --- SETUP DJANGO ENVIRONMENT ---
# This is crucial to allow this script to interact with your Django models.

# Get the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the absolute path of the project's root directory (subdomain-drishanti)
project_dir = os.path.abspath(script_dir)

# Add the project directory to Python's path
sys.path.append(project_dir)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
django.setup()

# --- IMPORT YOUR MODEL ---
from api.models import HomepageSlider

# --- DEFINE STATIC DATA FROM Hero.jsx ---
# This data is extracted directly from your React component.
slides_data = [
  {
    "title": "Homepage Banner 1 - Reimagined",
    "image_name": "banner1.webp",
    "text": "Rakshapotlis\nReimagined.",
    "description": "GOLD | SILVER | DIAMONDS",
    "button_1_text": "What is Rakshapotli",
    "button_1_link": "/what-is-rakshapotli",
    "button_2_text": "Discover Our Story",
    "button_2_link": "/about"
  },
  {
    "title": "Homepage Banner 2 - Reimagined Alt",
    "image_name": "banner2.webp",
    "text": "Rakshapotlis\nReimagined.",
    "description": "GOLD | SILVER | DIAMONDS",
    "button_1_text": "What is Rakshapotli",
    "button_1_link": "/what-is-rakshapotli",
    "button_2_text": "Discover Our Story",
    "button_2_link": "/about"
  },
  {
    "title": "Homepage Banner 3 - Baby",
    "image_name": "baby-banner.webp",
    "text": "Rakshapotlis\nReimagined.",
    "description": "GOLD | SILVER | DIAMONDS",
    "button_1_text": "What is Rakshapotli",
    "button_1_link": "/what-is-rakshapotli",
    "button_2_text": "Discover Our Story",
    "button_2_link": "/about"
  }
]

# --- DEFINE FILE PATHS ---
# Assumes this script is in 'subdomain-drishanti' and the frontend is a sibling directory 'drishanti-v2'
frontend_images_dir = os.path.abspath(os.path.join(project_dir, '..', 'drishanti-v2', 'public', 'images'))
django_media_dir = os.path.abspath(os.path.join(project_dir, 'media', 'homepage', 'slider'))

# --- MAIN POPULATION LOGIC ---
def populate_slider():
    print("Starting homepage slider population...")

    # Ensure the target media directory exists
    os.makedirs(django_media_dir, exist_ok=True)
    print(f"Media directory ensured at: {django_media_dir}")

    # Clear existing slides to avoid duplicates
    HomepageSlider.objects.all().delete()
    print("Cleared existing HomepageSlider entries.")

    for index, slide_item in enumerate(slides_data):
        print(f"Processing slide: {slide_item['title']}")

        # --- Image Handling ---
        source_image_path = os.path.join(frontend_images_dir, slide_item['image_name'])
        destination_image_path = os.path.join(django_media_dir, slide_item['image_name'])
        
        if not os.path.exists(source_image_path):
            print(f"  [!] WARNING: Source image not found at {source_image_path}. Skipping this slide.")
            continue

        # Copy the image file
        try:
            shutil.copy2(source_image_path, destination_image_path)
            print(f"  -> Copied image to {destination_image_path}")
        except Exception as e:
            print(f"  [!] ERROR: Could not copy image. {e}. Skipping this slide.")
            continue
            
        # The path to be stored in the ImageField
        django_image_path = os.path.join('homepage', 'slider', slide_item['image_name'])

        # --- Create Model Instance ---
        try:
            slider_instance, created = HomepageSlider.objects.update_or_create(
                title=slide_item['title'],
                defaults={
                    'slider_image': django_image_path,
                    'text': slide_item['text'].replace('\n', '\n'),
                    'subtitle': slide_item.get('description', ''),
                    'text_size': "clamp(32px, 5.5vw, 84px)",
                    'button_1_text': slide_item['button_1_text'],
                    'button_1_link': slide_item['button_1_link'],
                    'button_1_size': "text-[10px] md:text-[11px] 2xl:text-[15px]",
                    'button_2_text': slide_item['button_2_text'],
                    'button_2_link': slide_item['button_2_link'],
                    'button_2_size': "text-[10px] md:text-[11px] 2xl:text-[15px]",
                    'display_order': index,
                    'is_active': True,
                    'text_color': '#FFFFFF',
                    'text_alignment': 'left',
                    'button_1_color': '#b39168',
                    'button_2_color': '#FFFFFF',
                }
            )
            if created:
                print(f"  -> Successfully CREATED slide: {slider_instance.title}")
            else:
                print(f"  -> Successfully UPDATED slide: {slider_instance.title}")

        except Exception as e:
            print(f"  [!] ERROR: Could not create slide object in database. {e}")

    print("\nPopulation script finished.")

if __name__ == '__main__':
    populate_slider()
