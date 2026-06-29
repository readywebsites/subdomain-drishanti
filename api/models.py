from django.db import models
from ckeditor.fields import RichTextField

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email

# 📁 CATEGORY MODELS
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Sub Categories"

    def __str__(self):
        return f"{self.category.name} > {self.name}"


# 🔥 PRODUCT MODEL (ADMIN THI IMAGE ADD THASE)
class Product(models.Model):
    new_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    MATERIAL_CHOICES = (
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
    )

    TYPE_CHOICES = (
        ('Plain', 'Plain'),
        ('Stripes', 'Stripes'),
        ('Swastik', 'Swastik'),
        ('Nazariya', 'Nazariya'),
    )

    CATEGORY_CHOICES = (
        ('Kids', 'Kids'),
        ('Women', 'Women'),
        ('Adults', 'Adults'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)

    image = models.ImageField(upload_to='products/', help_text="Hero Image (Main Image)")
    detail_image_1 = models.ImageField(upload_to='products/', null=True, blank=True)
    detail_image_2 = models.ImageField(upload_to='products/', null=True, blank=True)
    detail_image_3 = models.ImageField(upload_to='products/', null=True, blank=True)
    detail_image_4 = models.ImageField(upload_to='products/', null=True, blank=True)
    detail_image_5 = models.ImageField(upload_to='products/', null=True, blank=True)
    detail_image_6 = models.ImageField(upload_to='products/', null=True, blank=True)
    detail_image_7 = models.ImageField(upload_to='products/', null=True, blank=True)
    detail_image_8 = models.ImageField(upload_to='products/', null=True, blank=True)
    detail_image_9 = models.ImageField(upload_to='products/', null=True, blank=True)
    video = models.FileField(upload_to='products/videos/', null=True, blank=True)
    gallery_images = models.JSONField(default=list, blank=True, help_text="List of additional product image URLs (Legacy)")
    description = RichTextField(blank=True)
    
    care_instructions = RichTextField(blank=True, null=True)
    activation_guidance = RichTextField(blank=True, null=True)
    product_details = RichTextField(blank=True, null=True)
    silver_weight = models.CharField(max_length=100, blank=True, null=True)
    chain_length = models.CharField(max_length=100, blank=True, null=True)
    size_chart = RichTextField(blank=True, null=True)
    style_number = models.CharField(max_length=100, blank=True, null=True)
    bracelet_size = models.CharField(max_length=100, blank=True, null=True)
    standard_preferable_chain_sizes = RichTextField(blank=True, null=True)

    stock = models.IntegerField(default=10)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='available_sizes')
    size = models.CharField(max_length=255, help_text="e.g., 5.5\" TO 7.2\" (1.8mm thickness)")

    def __str__(self):
        return f"{self.product.name} - {self.size}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    PAYMENT_CHOICES = (('Razorpay', 'Razorpay'), ('COD', 'Cash on Delivery'),)
    STATUS_CHOICES = (('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'),)
    SHIPPING_CHOICES = (('Standard', 'Standard Shipping'), ('Express', 'Express Shipping'),)
    session_id = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    billing_address = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_pincode = models.CharField(max_length=10, blank=True, null=True)
    subtotal = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    shipping_charge = models.IntegerField(default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.IntegerField(default=0)
    total = models.IntegerField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='Razorpay')
    shipping_method = models.CharField(max_length=50, choices=SHIPPING_CHOICES, default='Standard')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    courier_partner = models.CharField(max_length=100, blank=True, null=True)
    delivery_estimate = models.DateField(blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} — {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Wishlist(models.Model):
    session_id = models.CharField(max_length=100, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_id', 'product')

    def __str__(self):
        return f"{self.session_id} - {self.product.name}"

class Cart(models.Model):
    session_id = models.CharField(max_length=100, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=50, default='Standard')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_id', 'product', 'size')

    def __str__(self):
        return f"{self.session_id} - {self.product.name} ({self.size})"

class CustomizedProduct(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='customized/')
    description = RichTextField(blank=True, null=True)
    badge = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Bestseller, Premium, New")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.email}"

class HomepageSlider(models.Model):
    ALIGNMENT_CHOICES = (('left', 'Left'), ('center', 'Center'), ('right', 'Right'),)
    title = models.CharField(max_length=200, help_text="Internal title for identifying the slide")
    slider_image = models.ImageField(upload_to='homepage/slider/', help_text="Recommended size: 1920x800px")
    text = models.TextField(blank=True, help_text="Main text/headline for the slide")
    subtitle = models.CharField(max_length=200, blank=True, help_text="Subtitle text, e.g., 'GOLD | SILVER | DIAMONDS'")
    text_color = models.CharField(max_length=7, default='#FFFFFF', help_text="Color of the main text (hex code, e.g., #FFFFFF)")
    text_alignment = models.CharField(max_length=10, choices=ALIGNMENT_CHOICES, default='center')
    text_size = models.CharField(max_length=100, blank=True, help_text="CSS font-size value for the main text (e.g., 'clamp(32px, 5.5vw, 84px)')")
    button_1_text = models.CharField(max_length=50, blank=True)
    button_1_link = models.URLField(max_length=200, blank=True)
    button_1_color = models.CharField(max_length=7, default='#000000', help_text="Background color of button 1 (hex code)")
    button_1_size = models.CharField(max_length=100, blank=True, help_text="Tailwind classes for button 1 font size")
    button_2_text = models.CharField(max_length=50, blank=True)
    button_2_link = models.URLField(max_length=200, blank=True)
    button_2_color = models.CharField(max_length=7, default='#FFFFFF', help_text="Background color of button 2 (hex code)")
    button_2_size = models.CharField(max_length=100, blank=True, help_text="Tailwind classes for button 2 font size")
    display_order = models.PositiveIntegerField(default=0, help_text="Order of the slide on the homepage (0 is first)")
    is_active = models.BooleanField(default=True, help_text="Uncheck this to hide the slide without deleting it")

    class Meta:
        verbose_name = "Homepage Slide"
        verbose_name_plural = "Homepage Slides"
        ordering = ['display_order']

    def __str__(self):
        return self.title

class LuxuryCollection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to='luxury/collections/', help_text="Main image for the collection page")
    video_url = models.URLField(blank=True, null=True, help_text="Optional video URL for the collection")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class LuxuryProduct(models.Model):
    collection = models.ForeignKey(LuxuryCollection, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='luxury/products/')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.collection.name} - {self.name}"

class GoldSilverSection(models.Model):
    SECTION_CHOICES = (('gold', 'Gold'), ('silver', 'Silver'),)
    section_type = models.CharField(max_length=10, choices=SECTION_CHOICES, unique=True, help_text="Identifier for the section (Gold or Silver)")
    title = models.CharField(max_length=100)
    title_suffix = models.CharField(max_length=100, default='Collection', help_text="e.g., 'Collection'")
    subtitle = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='goldsilver/', help_text="Background image for the section")
    button_text = models.CharField(max_length=50, default='EXPLORE')
    button_link = models.CharField(max_length=200, help_text="URL link for the button (e.g., /shop/gold)")
    title_color = models.CharField(max_length=7, default='#000000')
    collection_color = models.CharField(max_length=7, default='#000000')
    text_color = models.CharField(max_length=7, default='#000000')
    line_color = models.CharField(max_length=7, default='#000000')
    button_bg_color = models.CharField(max_length=7, default='#000000')
    object_position = models.CharField(max_length=50, default='object-center', help_text="Tailwind class for image positioning (e.g., 'object-bottom')")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Gold/Silver Section"
        verbose_name_plural = "Gold/Silver Sections"
        ordering = ['display_order']

    def __str__(self):
        return self.title

class ComponentsSection(models.Model):
    title = models.CharField(max_length=200, default="THE ANATOMY OF SACRED CRAFT")
    subtitle_part_1 = models.CharField(max_length=200, default="Components of")
    subtitle_part_2 = models.CharField(max_length=200, default="Rakshapotli")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Components Section"
        verbose_name_plural = "Components Sections"

    def __str__(self):
        return self.title

class ComponentCard(models.Model):
    section = models.ForeignKey(ComponentsSection, on_delete=models.CASCADE, related_name='cards')
    display_id = models.CharField(max_length=2, help_text="The two-digit number, e.g., '01'")
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='rakshapotli_components/')
    icon_name = models.CharField(max_length=50, help_text="Name of the lucide-react icon (e.g., 'Gem', 'Sparkles')")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Component Card"
        verbose_name_plural = "Component Cards"
        ordering = ['display_order']

    def __str__(self):
        return self.title

class OccasionsSection(models.Model):
    title = models.CharField(max_length=200, default="Find the Perfect Rakshapotli for Every Occasion")
    subtitle = models.CharField(max_length=200, default="Thoughtfully curated gifts for life's beautiful moments.")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Occasions Section"
        verbose_name_plural = "Occasions Sections"

    def __str__(self):
        return self.title

class OccasionCard(models.Model):
    section = models.ForeignKey(OccasionsSection, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=100)
    icon_name = models.CharField(max_length=50, help_text="Name of the lucide-react icon (e.g., 'Baby', 'Heart')")
    hover_image = models.ImageField(upload_to='occasions/')
    link = models.CharField(max_length=200, default="#")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Occasion Card"
        verbose_name_plural = "Occasion Cards"
        ordering = ['display_order']

    def __str__(self):
        return self.title

class FAQSection(models.Model):
    title = models.CharField(max_length=200, default="Frequently Asked Questions")
    button_text = models.CharField(max_length=100, default="Connect With Us")
    button_link = models.CharField(max_length=200, default="/contact")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ Section"
        verbose_name_plural = "FAQ Sections"

    def __str__(self):
        return self.title

class FAQItem(models.Model):
    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, related_name='faq_items')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"
        ordering = ['display_order']

    def __str__(self):
        return self.question

# 💬 Testimonials Section
class TestimonialsSection(models.Model):
    title = models.CharField(max_length=100, default="Human Impressions")
    subtitle = models.CharField(max_length=100, default="Lived Experiences")
    bottom_text = models.CharField(max_length=100, default="Blessed Globally")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Testimonials Section"
        verbose_name_plural = "Testimonials Sections"

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    section = models.ForeignKey(TestimonialsSection, on_delete=models.CASCADE, related_name='testimonials')
    name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Rating from 1 to 5")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['display_order']

    def __str__(self):
        return self.name

class Footer(models.Model):
    section1_title = models.CharField(max_length=200)
    section1_description = models.TextField()
    section1_subscription_box_title = models.CharField(max_length=200)
    section1_subscription_box_description = models.TextField()

    class Meta:
        verbose_name = "Footer Section"
        verbose_name_plural = "Footer Sections"

    def __str__(self):
        return "Footer Configuration"

class FooterSecondSection(models.Model):
    footer = models.OneToOneField(Footer, on_delete=models.CASCADE, related_name='section_two')
    copyright_text_1 = models.CharField(max_length=200, default="© 2026 Drishanti. Elegant Luxury.")
    copyright_text_2 = models.CharField(max_length=200, default="Crafted in India, Consecrated for the World.")

    class Meta:
        verbose_name = "Footer Second Section"
        verbose_name_plural = "Footer Second Sections"

    def __str__(self):
        return f"Section Two for {self.footer.section1_title}"

class FooterIcon(models.Model):
    footer = models.ForeignKey(Footer, on_delete=models.CASCADE, related_name='icons')
    name = models.CharField(max_length=50, help_text="e.g., Facebook, Instagram")
    icon_class = models.CharField(max_length=100, help_text="e.g., fa fa-facebook, fab fa-instagram (Font Awesome classes)")
    link = models.URLField(max_length=200)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Footer Icon"
        verbose_name_plural = "Footer Icons"
        ordering = ['display_order']

    def __str__(self):
        return f"{self.name} ({self.footer.section1_title})"

class FooterMenu(models.Model):
    section_two = models.ForeignKey(FooterSecondSection, on_delete=models.CASCADE, related_name='menus', null=True, blank=True)
    title = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Footer Menu"
        verbose_name_plural = "Footer Menus"
        ordering = ['display_order']

    def __str__(self):
        return f"{self.title} (Footer Section Two)"

    def get_menu_items_display(self):
        return ", ".join([item.text for item in self.items.all()])
    get_menu_items_display.short_description = "Menu Items"

class FooterMenuItem(models.Model):
    menu = models.ForeignKey(FooterMenu, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=100)
    link = models.CharField(max_length=200) # Using CharField for internal links like /shop/gold
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Footer Menu Item"
        verbose_name_plural = "Footer Menu Items"
        ordering = ['display_order']

    def __str__(self):
        return f"{self.text} ({self.menu.title})"

class AboutPage(models.Model):
    hero_image = models.ImageField(upload_to='about/', blank=True, null=True)
    hero_quote = models.TextField(blank=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Pages"

    def __str__(self):
        return "About Us Page"

class AboutSection(models.Model):
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='sections')
    image = models.ImageField(upload_to='about/')
    content = RichTextField()
    image_position = models.CharField(max_length=5, choices=(('left', 'Left'), ('right', 'Right')), default='right')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Section {self.display_order} for {self.page}"

    def save(self, *args, **kwargs):
        if not self.pk: # Only on creation
            last_section = AboutSection.objects.filter(page=self.page).order_by('-display_order').first()
            if last_section:
                self.display_order = last_section.display_order + 1
                if last_section.image_position == 'left':
                    self.image_position = 'right'
                else:
                    self.image_position = 'left'
            else:
                self.display_order = 1
                self.image_position = 'right' # First section image on the right
        super().save(*args, **kwargs)

class ContactPage(models.Model):
    title = models.CharField(max_length=200, default="Get in Touch")
    subtitle = models.TextField(blank=True)
    business_details_title = models.CharField(max_length=200, default="Business Details")
    business_details_subtitle = models.TextField(blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    hours = models.CharField(max_length=100, blank=True)
    whatsapp_support_title = models.CharField(max_length=200, default="WhatsApp support")
    whatsapp_support_subtitle = models.TextField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Contact Page"
        verbose_name_plural = "Contact Pages"

    def __str__(self):
        return "Contact Page"

class Policy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = RichTextField()
    last_updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return self.title