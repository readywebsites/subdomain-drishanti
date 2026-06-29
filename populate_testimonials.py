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
from api.models import TestimonialsSection, Testimonial

# --- DEFINE STATIC DATA ---
section_data = {
    "title": "Human Impressions",
    "subtitle": "Lived Experiences",
    "bottom_text": "Blessed Globally",
}

testimonials_data = [
    { "name": "Geeta Sata", "review": "Realy u have superb vision, brain and tt spark to work in yr field.. I love all the things you put very creative..", "rating": 5 },
    { "name": "Rahul Jain", "review": "Hi harshmi, how r you dear. I absolutely loved loved the Rakshapotli. The finish, the quality of red potli is amazing. I was little worried as I have seen many enamel work everywhere that cannot achieve it's best finish, but your rakshapotli is superbly done. Thankyou for all your efforts and being sucha a good listener right from the start. I will proudly recommend you to my circle. Also I loved the box you sent in. The feel of whole package is so good ❤️ Keep up the great work. Will let me know my bhabhi's review once we gift them 🤗🤗", "rating": 5 },
    { "name": "Hardi Shah", "review": "I have been seeing rakshapotli in gold, diamond and many other fancy medium but none made an appeal to me. Always wanted one for my brother to tie him as a Rakhi. Had been following harshmi works since ages as we were from same college, I always found her work to be uniquely symbolic to person for whom she made.. this added more emotional value to jewellery. When I saw her rakshapotli it convinced me that I need this for my brother.. She customised each minute details with lots of love and perfection! Each small details were discussed and elaborated well. And when it was delivered to me, it was perfectly made as discussed and imagined! Thank you harshmi for fabricating so well! Hope to get many more unique Jewelry done with you ❤️😊", "rating": 5 },
    { "name": "Rashmi Patwardhan", "review": "The first time I saw the Raksha potli...I fell in love with it and wanted it right away!! Harshmi helped me customise it as per my needs and the complete journey from Color selection to the material was enigmatic!! The product I got was perfect and loved every bit of it. We went through an awesome journey to have the BLESSED potli in in no time!! Love love love it 😍", "rating": 5 },
    { "name": "Priyal Doshi", "review": "Hi Harshmi Thank you so much for the lovely Rakshapotli 😍00 It's simply awesome 🤗❤️ really really loved it alot 🥰🥰 Will wear tomorrow morning n let u know 😊", "rating": 5 },
    { "name": "Ankit Shah", "review": "Best gift 🎁 for children’s and family, unique art of work with the blend of spiritual idea", "rating": 5 },
]

# --- MAIN POPULATION LOGIC ---
def populate_testimonials():
    print("Starting Testimonials section population...")
    
    # --- Clear old data ---
    TestimonialsSection.objects.all().delete()
    Testimonial.objects.all().delete()
    print("Cleared existing Testimonials Section and Items.")

    # --- Populate Header Section ---
    section, created = TestimonialsSection.objects.get_or_create(id=1, defaults=section_data)
    if created:
        print("-> Successfully CREATED section header.")
    else:
        print("-> Successfully UPDATED section header.")

    # --- Populate Testimonial Items for the Section ---
    for index, item_data in enumerate(testimonials_data):
        try:
            item, created = Testimonial.objects.update_or_create(
                section=section,
                name=item_data['name'],
                defaults={
                    'review': item_data['review'],
                    'rating': item_data['rating'],
                    'display_order': index,
                    'is_active': True,
                }
            )
            if created:
                print(f"  -> Successfully CREATED Testimonial: {item.name}")
            else:
                print(f"  -> Successfully UPDATED Testimonial: {item.name}")

        except Exception as e:
            print(f"  [!] ERROR: Could not create Testimonial object in database. {e}")

    print("\nPopulation script finished.")

if __name__ == '__main__':
    populate_testimonials()
