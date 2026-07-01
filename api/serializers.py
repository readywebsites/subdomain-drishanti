from rest_framework import serializers
from .models import (
    Product, Category, SubCategory, Order, OrderItem, Coupon, 
    CustomizedProduct, Wishlist, Cart, ContactMessage, 
    NewsletterSubscription, HomepageSlider, GoldSilverSection, ProductSize,
    ComponentsSection, ComponentCard, OccasionsSection, OccasionCard,
    FAQSection, FAQItem, TestimonialsSection, Testimonial,
    Footer, FooterIcon, FooterMenu, FooterMenuItem, FooterSecondSection,
    AboutPage, AboutSection, ContactPage, Policy
)

class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('size',)

class ProductSerializer(serializers.ModelSerializer):
    available_sizes = ProductSizeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        lookup_field = 'slug'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'subcategories']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_details = ProductSerializer(source='product', read_only=True)
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_details', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class CustomizedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomizedProduct
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)
    product_discount_price = serializers.IntegerField(source='product.discount_price', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)

    class Meta:
        model = Wishlist
        fields = [
            'id',
            'session_id',
            'product',
            'product_name',
            'product_image',
            'product_price',
            'product_discount_price',
            'product_slug',
            'created_at'
        ]

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)
    product_discount_price = serializers.IntegerField(source='product.discount_price', read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 
            'session_id', 
            'product', 
            'product_name', 
            'product_image', 
            'product_price', 
            'product_discount_price', 
            'quantity', 
            'size', 
            'created_at'
        ]

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = '__all__'

class HomepageSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepageSlider
        fields = '__all__'

class GoldSilverSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldSilverSection
        fields = '__all__'

class ComponentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentCard
        fields = ('display_id', 'title', 'description', 'image', 'icon_name', 'display_order')

class ComponentsSectionSerializer(serializers.ModelSerializer):
    cards = ComponentCardSerializer(many=True, read_only=True)

    class Meta:
        model = ComponentsSection
        fields = ('id', 'title', 'subtitle_part_1', 'subtitle_part_2', 'cards')

class OccasionCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccasionCard
        fields = ('title', 'icon_name', 'hover_image', 'link', 'display_order')

class OccasionsSectionSerializer(serializers.ModelSerializer):
    cards = OccasionCardSerializer(many=True, read_only=True)

    class Meta:
        model = OccasionsSection
        fields = ('id', 'title', 'subtitle', 'cards')

class FAQItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQItem
        fields = ('question', 'answer', 'display_order')

class FAQSectionSerializer(serializers.ModelSerializer):
    faq_items = FAQItemSerializer(many=True, read_only=True)

    class Meta:
        model = FAQSection
        fields = ('id', 'title', 'button_text', 'button_link', 'faq_items')

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ('name', 'review', 'rating', 'display_order')

class TestimonialsSectionSerializer(serializers.ModelSerializer):
    testimonials = TestimonialSerializer(many=True, read_only=True)

    class Meta:
        model = TestimonialsSection
        fields = ('id', 'title', 'subtitle', 'bottom_text', 'testimonials')

class FooterIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterIcon
        fields = ('name', 'icon_class', 'link', 'display_order')

class FooterMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterMenuItem
        fields = ('text', 'link', 'display_order')

class FooterMenuSerializer(serializers.ModelSerializer):
    items = FooterMenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = FooterMenu
        fields = ('title', 'display_order', 'items')

class FooterSecondSectionSerializer(serializers.ModelSerializer):
    menus = FooterMenuSerializer(many=True, read_only=True)

    class Meta:
        model = FooterSecondSection
        fields = ('copyright_text_1', 'copyright_text_2', 'menus')

class FooterSerializer(serializers.ModelSerializer):
    icons = FooterIconSerializer(many=True, read_only=True)
    section_two = FooterSecondSectionSerializer(read_only=True) # Use the new serializer

    class Meta:
        model = Footer
        fields = (
            # Section 1 Fields
            'section1_title',
            'section1_description',
            'section1_subscription_box_title',
            'section1_subscription_box_description',
            'icons',
            # Section 2 Fields
            'section_two', # Reference the nested serializer
        )

class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = ('image', 'content', 'image_position', 'display_order')

class AboutPageSerializer(serializers.ModelSerializer):
    sections = AboutSectionSerializer(many=True, read_only=True)

    class Meta:
        model = AboutPage
        fields = ('hero_image', 'hero_quote', 'sections')

class ContactPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage
        fields = '__all__'

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'