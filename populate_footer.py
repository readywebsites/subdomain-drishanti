import os
import django
import nested_admin

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Footer, FooterIcon, FooterMenu, FooterMenuItem, FooterSecondSection

def populate_footer():
    print("Populating Footer and Footer Icons with exact content from screenshot...")

    # Create or get the single Footer instance
    footer, created = Footer.objects.get_or_create(
        pk=1, # Assuming a single footer instance
        defaults={
            'section1_title': "DRISHANTI",
            'section1_description': "Its more than a brand. It is a way of honouring a tradition, preserving its meaning, and sharing it with future generations.",
            'section1_subscription_box_title': "THE INNER CIRCLE",
            'section1_subscription_box_description': "Join us for exclusive spiritual insights and early access to our limited collections.",
        }
    )

    if created:
        print("Created Footer instance.")
    else:
        print("Footer instance already exists. Updating with screenshot content.")
        footer.section1_title = "DRISHANTI"
        footer.section1_description = "Its more than a brand. It is a way of honouring a tradition, preserving its meaning, and sharing it with future generations."
        footer.section1_subscription_box_title = "THE INNER CIRCLE"
        footer.section1_subscription_box_description = "Join us for exclusive spiritual insights and early access to our limited collections."
        footer.save()

    # Create or get the single FooterSecondSection instance
    footer_second_section, created_section_two = FooterSecondSection.objects.get_or_create(
        footer=footer,
        defaults={
            'copyright_text_1': "© 2026 Drishanti. Elegant Luxury.",
            'copyright_text_2': "Crafted in India, Consecrated for the World.",
        }
    )

    if created_section_two:
        print("Created FooterSectionTwo instance.")
    else:
        print("FooterSecondSection instance already exists. Updating with screenshot content.")
        footer_second_section.copyright_text_1 = "© 2026 Drishanti. Elegant Luxury."
        footer_second_section.copyright_text_2 = "Crafted in India, Consecrated for the World."
        footer_second_section.save()

    # Clear existing icons for this footer to avoid duplicates on re-run
    footer.icons.all().delete()
    print("Cleared existing Footer Icons.")

    # Create Footer Icons based on screenshot
    icons_data = [
        {"name": "Instagram", "icon_class": "fab fa-instagram", "link": "https://www.instagram.com/drishantiofficial", "display_order": 1},
        {"name": "Facebook", "icon_class": "fab fa-facebook-f", "link": "https://www.facebook.com/drishantiofficial", "display_order": 2},
        {"name": "Twitter", "icon_class": "fab fa-twitter", "link": "https://twitter.com/drishantiofficial", "display_order": 3},
    ]

    for data in icons_data:
        FooterIcon.objects.create(footer=footer, **data)
        print(f"Created Footer Icon: {data['name']}")

    # Clear existing menus for this footer second section to avoid duplicates on re-run
    footer_second_section.menus.all().delete()
    print("Cleared existing Footer Menus.")

    # Create Footer Menus and Menu Items
    menus_data = [
        {
            "title": "Collections",
            "display_order": 1,
            "items": [
                {"text": "Rakshapotli Gold", "link": "/shop/gold", "display_order": 1},
                {"text": "Sterling Silver", "link": "/shop/silver", "display_order": 2},
            ]
        },
        {
            "title": "The House",
            "display_order": 2,
            "items": [
                {"text": "Our Story", "link": "/about", "display_order": 1},
            ]
        },
        {
            "title": "Client Care",
            "display_order": 3,
            "items": [
                {"text": "Shipping & Returns", "link": "/policy/shipping-returns", "display_order": 1},
                {"text": "Privacy Policy", "link": "/policy/privacy-policy", "display_order": 2},
                {"text": "Terms of Service", "link": "/policy/terms-of-service", "display_order": 3},
                {"text": "FAQ", "link": "/faq", "display_order": 4},
            ]
        },
        {
            "title": "Inquiry",
            "display_order": 4,
            "items": [
                {"text": "Unique Heights, Poonam Gardens, Mira Road - 401107", "link": "#", "display_order": 1},
                {"text": "+91 9920122216", "link": "tel:+919920122216", "display_order": 2},
                {"text": "drishantiofficial@gmail.com", "link": "mailto:drishantiofficial@gmail.com", "display_order": 3},
            ]
        },
    ]

    for menu_data in menus_data:
        menu = FooterMenu.objects.create(
            section_two=footer_second_section,
            title=menu_data["title"],
            display_order=menu_data["display_order"]
        )
        print(f"Created Footer Menu: {menu.title}")
        for item_data in menu_data["items"]:
            FooterMenuItem.objects.create(menu=menu, **item_data)
            print(f"  Created Menu Item: {item_data['text']}")

    print("Footer and Footer Icons population complete with screenshot content.")

if __name__ == '__main__':
    populate_footer()
