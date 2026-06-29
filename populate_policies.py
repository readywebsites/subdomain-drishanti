import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Policy

def populate_policies():
    # Clear existing data
    Policy.objects.all().delete()
    print("Cleared existing Policy data.")

    # Shipping & Returns
    shipping_content = """
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Shipping Policy</h2>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li><strong>Domestic: </strong>Ready-to-ship products are dispatched within 3–7 business days.</li>
        <li><strong>International:</strong> At present, we only ship within domestic regions; international shipping is not yet available.</li>
        <li>Tracking details will be shared once the order is dispatched.</li>
        <li>Delivery timelines may vary depending on location and courier services.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Pre-Dispatch Approval</h2>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>Photographs or videos of customised orders may be shared before dispatch.</li>
        <li>Certain components such as chains, extension chains, hooks, clasps, and locks may vary slightly based on availability.</li>
        <li>Such changes will not affect the overall design, quality, or purpose of the product.</li>
        <li>Once approved and dispatched, these variations shall not be considered grounds for return or refund.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Returns & Exchanges</h2>
      <p>Return requests must be initiated within 7 days of delivery.</p>
      <br />
      <p class="font-bold">Returns will only be considered if:</p>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>The product is received damaged.</li>
        <li>The product is defective.</li>
        <li>An incorrect product has been delivered.</li>
        <li>The package is missing components listed in the order.</li>
        <li>The delivered product significantly differs from the approved design or product description.</li>
      </ul>
      <p class="font-bold mt-8">To be eligible:</p>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>An uninterrupted unboxing video is mandatory.</li>
        <li>The product must be unused and unworn.</li>
        <li>All original packaging, certificates, tags, authenticity cards, and accompanying materials must be returned.</li>
        <li>Returned products will undergo inspection before approval.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6"> Non-Returnable Items</h2>
      <p>The following items are not eligible for return or refund:</p>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>Customised or personalised products.</li>
        <li>Made-to-order products.</li>
        <li>Bulk, Prabhavna, corporate gifting, and special project orders.</li>
        <li>Products approved by the customer before dispatch.</li>
        <li>Products showing signs of wear, misuse, alteration, repair, or damage after delivery.</li>
        <li>Products purchased during promotional or clearance sales.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6"> Refunds</h2>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>Refunds are issued only for approved return requests.</li>
        <li>Approved refunds will be processed within 7–14 business days after inspection and approval.</li>
        <li>Original shipping charges, payment gateway charges, taxes, packaging charges, insurance charges, and handling charges are non-refundable.</li>
        <li>Return shipping charges must be borne by the customer.</li>
        <li>Applicable charges will be deducted before processing the refund.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Exchanges</h2>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>We do not offer direct exchanges.</li>
        <li>If you would like a different product, please initiate a return (if eligible) and place a new order separately.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Damaged or Incorrect Orders</h2>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>Please notify us within 48 hours of delivery.</li>
        <li>The original unboxing video and supporting photographs may be required.</li>
        <li>Upon verification, DRISHANTI will determine the appropriate resolution, including repair, replacement, or refund.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6"> Handcrafted Variations</h2>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>Every DRISHANTI creation is handcrafted.</li>
        <li>Minor variations in thread work, enamel, engraving, colour, weight, or handcrafted detailing are natural characteristics of handmade products and are not considered defects.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6"> Product Care & Refresh Service</h2>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>Daily wear may result in gradual ageing of thread, enamel, ceramic, plating, or surface finishes.</li>
        <li>Such wear is considered normal and not a manufacturing defect.</li>
        <li>If your Rakshapotli requires refreshing, restoration, or replacement of the red ceramic/enamel due to genuine daily wear, please contact us.</li>
        <li>Repairs may be offered at minimal cost or, in certain cases, at no product charge, subject to evaluation.</li>
        <li>Shipping and courier charges for repair services shall be borne by the customer.</li>
        <li>* All repair requests are reviewed individually.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6"> Price Validity</h2>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>Quotations for customised orders are valid for 7 days due to fluctuations in precious metal prices.</li>
      </ul>
    </section>
    """

    # Privacy Policy
    privacy_content = """
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Information We Collect</h2>
      <p>DRISHANTI respects your privacy and is committed to protecting your personal data. We collect information such as your name, email, shipping address, and payment details only to fulfill your orders and enhance your experience with us.</p>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">How We Use Your Data</h2>
      <p>Your information is used strictly for:</p>
      <ul class="list-disc pl-6 space-y-4 mt-4">
        <li>Processing and delivering your sacred pieces.</li>
        <li>Sending updates regarding your order status.</li>
        <li>Providing spiritual insights and collection previews via our newsletter (if subscribed).</li>
        <li>Ensuring the security and integrity of our website.</li>
      </ul>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Data Security</h2>
      <p>We implement industry-standard security measures to safeguard your information. We do not sell, trade, or otherwise transfer your personally identifiable information to outside parties.</p>
    </section>
    """

    # Terms of Service
    terms_content = """
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Agreement to Terms</h2>
      <p>By accessing the DRISHANTI website and purchasing our products, you agree to be bound by these Terms of Service. These terms apply to all users of the site, including browsers, customers, and contributors.</p>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Product Integrity</h2>
      <p>While we strive for absolute accuracy, please note that each piece is handcrafted and may have slight variations. These are not flaws but marks of authenticity and the artisan's hand.</p>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Intellectual Property</h2>
      <p>The content on this website, including designs, text, and imagery, is the intellectual property of DRISHANTI and is protected by copyright laws. Any unauthorized use is strictly prohibited.</p>
    </section>
    <section>
      <h2 class="text-2xl font-serif text-primary mb-6">Governing Law</h2>
      <p>These terms shall be governed by and construed in accordance with the laws of India, with jurisdiction in Mumbai.</p>
    </section>
    """

    policies = [
        {"title": "Shipping & Returns", "slug": "shipping-returns", "content": shipping_content},
        {"title": "Privacy Policy", "slug": "privacy-policy", "content": privacy_content},
        {"title": "Terms of Service", "slug": "terms-of-service", "content": terms_content},
    ]

    for policy_data in policies:
        Policy.objects.create(
            title=policy_data["title"],
            slug=policy_data["slug"],
            content=policy_data["content"]
        )
        print(f"Created Policy: {policy_data['title']}")

    print("Policies population complete.")

if __name__ == '__main__':
    populate_policies()
