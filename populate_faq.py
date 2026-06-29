

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
from api.models import FAQSection, FAQItem

# --- DEFINE STATIC DATA ---
section_data = {
    "title": "Frequently Asked Questions",
    "button_text": "Connect With Us",
    "button_link": "/contact",
}

faq_data = [
    {
      "question": "What is Rakshapotli?",
      "answer": "Rakshapotli is a symbol of protection, awareness, and inner intention traditionally worn on the right wrist. Deeply rooted in Jain culture, it is worn as a quiet reminder of one’s values and personal commitments."
    },
    {
      "question": "Is Rakshapotli only for Jains?",
      "answer": "Rakshapotli originates from Jain traditions and values. While we preserve its authenticity and roots with deep respect, our vision at DRISHANTI goes beyond religion. We welcome everyone who connects with its philosophy of peace, awareness, and mindful living."
    },
    {
      "question": "What is inside a DRISHANTI Rakshapotli?",
      "answer": "Every DRISHANTI Rakshapotli contains Vasakshep carefully encapsulated within the centrepotli. The Vasakshep is respectfully sourced from sacred Jain tirths such as Shankheshwar Parshwanath, Mahudi, Shatrunjay Palitana, and other spiritually significant places, allowing their blessings and essence to be carried closely with you every day."
    },
    {
      "question": "Why is Rakshapotli worn on the right wrist?",
      "answer": "Traditionally, Rakshapotli is worn on the right wrist as a symbol of intention, discipline, and spiritual grounding."
    },
    {
      "question": "What materials are used in DRISHANTI Rakshapotlis?",
      "answer": "Our pieces are crafted in 18kt Gold or 925 Hallmarked Silver, and certified Diamonds."
    },
    {
      "question": "Are your products hallmarked and certified?",
      "answer": "Yes. All Gold products are BIS Hallmarked with HUID certification."
    },
    {
      "question": "What is German Ceramic processing?",
      "answer": "German Ceramic processing is our signature imported technique exclusively used by DRISHANTI to enhance colour longevity, smoothness, durability, and everyday wearability of the Rakshapotli. This process helps create a refined finish that is comfortable on the skin and scratch resistant."
    },
    {
      "question": "Are the Rakshapotlis suitable for daily wear?",
      "answer": "Yes. Every piece is thoughtfully designed for comfortable everyday wear with smooth rounded finishes and durable construction."
    },
    {
      "question": "How do I activate my Rakshapotli?",
      "answer": "You may get it Abhimantrit from Maharaj Saheb, keep it during Siddhachakra Pujan, place it in your home mandir, or simply wear it with prayer and intention. More than ritual, it is your belief that strengthens its connection."
    },
    {
      "question": "Can Rakshapotli be gifted?",
      "answer": "Absolutely. Rakshapotli makes for a deeply meaningful gift for loved ones across different stages of life."
    },
    {
      "question": "Will my silver Rakshapotli tarnish over time?",
      "answer": "Silver is a precious metal with a natural characteristic to react with air, moisture, and surroundings over time. At DRISHANTI, our root ethics are built on 100% honesty. We do not sell through misleading marketing silver will “never tarnish.” All our silver Rakshapotlis are finished with anti tarnish protection to help enhance longevity and everyday wearability. However, regular wear, surroundings, moisture, perfumes, and storage conditions naturally affect silver over time. Interestingly, silver shines best when worn regularly. Daily wear keeps it active and radiant. When left unused for long periods in cupboards or exposed to moisture and air, it may gradually oxidise and darken. This does not mean the product is damaged. Silver can always be cleaned and restored to its original shine with proper care."
    },
    {
      "question": "Can I store the product in the DRISHANTI box?",
      "answer": "The DRISHANTI box is designed primarily for presentation and gifting. For long term care, airtight storage is recommended."
    },
    {
      "question": "Can I wear my Rakshapotli while bathing or swimming?",
      "answer": "We recommend removing your Rakshapotli while bathing in areas with harsh water, during swimming, or while doing rough activities to help preserve its finish and longevity over time."
    },
    {
      "question": "Do you offer shipping across India?",
      "answer": "Yes. We offer secure shipping across India."
    },
    {
      "question": "Is the jewellery insured during shipping?",
      "answer": "Yes. All fine jewellery shipments are securely packed and insured during transit."
    },
    {
      "question": "How long will my order take to arrive?",
      "answer": "Delivery timelines may vary depending on product availability and customisation. Estimated timelines will be shared during order confirmation."
    },
    {
      "question": "Can I customise my Rakshapotli?",
      "answer": "Yes. Selected Rakshapotli can be customised in Gold, Silver, available thread colours, chain styles, symbols, and sizing. For customisation requests, personalised gifting, or special requirements, you may connect with us through WhatsApp or email, and our team will guide you through the available options."
    },
    {
      "question": "Do you create custom gifting pieces?",
      "answer": "Yes. We create personalised gifting pieces designed around your intent, occasion, or meaningful ideas. Connect with our team to explore possibilities, timelines, design directions, available alternatives, and customisation charges if any."
    }
]

# --- MAIN POPULATION LOGIC ---
def populate_faq():
    print("Starting FAQ section population...")
    
    # --- Clear old data ---
    FAQSection.objects.all().delete()
    FAQItem.objects.all().delete()
    print("Cleared existing FAQ Section and Items.")

    # --- Populate Header Section ---
    section, created = FAQSection.objects.get_or_create(id=1, defaults=section_data)
    if created:
        print("-> Successfully CREATED section header.")
    else:
        print("-> Successfully UPDATED section header.")

    # --- Populate FAQ Items for the Section ---
    for index, item_data in enumerate(faq_data):
        try:
            item, created = FAQItem.objects.update_or_create(
                section=section,
                question=item_data['question'],
                defaults={
                    'answer': item_data['answer'],
                    'display_order': index,
                    'is_active': True,
                }
            )
            if created:
                print(f"  -> Successfully CREATED FAQ: {item.question}")
            else:
                print(f"  -> Successfully UPDATED FAQ: {item.question}")

        except Exception as e:
            print(f"  [!] ERROR: Could not create FAQ object in database. {e}")

    print("\nPopulation script finished.")

if __name__ == '__main__':
    populate_faq()
