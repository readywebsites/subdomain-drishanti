import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import ContactPage

def populate_contact_page():
    # Clear existing data
    ContactPage.objects.all().delete()
    print("Cleared existing Contact Page data.")

    # Create the ContactPage instance
    ContactPage.objects.create(
        title="Get in Touch",
        subtitle="Have a question about our collections, bespoke orders, or a gifting request? Send us a message and our team will respond as soon as possible.",
        business_details_title="Business Details",
        business_details_subtitle="Drishanti is available for custom orders, bulk gifting, and personal consultations. Reach out anytime, and we'll assist you with our timeless collection.",
        address="Unique Heights, Poonam Gardens, Miraroad - 401107",
        phone="+91 9920122216",
        email="drishantiofficial@gmail.com",
        hours="Mon - Sat: 10am - 7pm",
        whatsapp_support_title="WhatsApp support",
        whatsapp_support_subtitle="Send a message directly on WhatsApp for order queries and custom requests.",
        whatsapp_number="919900112233"
    )
    print("Contact Page population complete.")

if __name__ == '__main__':
    populate_contact_page()
