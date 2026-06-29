from django import forms
from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from django.utils.html import format_html
from .models import (
    Product, Order, OrderItem, Wishlist, Cart, Coupon, Category, SubCategory, 
    ProductSize, CustomizedProduct, ContactMessage, NewsletterSubscription, 
    HomepageSlider, GoldSilverSection, ComponentsSection, ComponentCard,
    OccasionsSection, OccasionCard, FAQSection, FAQItem,
    TestimonialsSection, Testimonial,
    Footer, FooterSecondSection, FooterIcon, FooterMenu, FooterMenuItem,
    AboutPage, AboutSection, ContactPage, Policy
)

class NoDeleteAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class NoDeleteNestedAdmin(NestedModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(NoDeleteAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)

# 📂 CATEGORY ADMIN
@admin.register(Category)
class CategoryAdmin(NoDeleteAdmin):
    list_display = ('id', 'name', 'slug', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(NoDeleteAdmin):
    list_display = ('id', 'name', 'category', 'slug', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name',)
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CustomizedProduct)
class CustomizedProductAdmin(NoDeleteAdmin):
    list_display = ('id', 'title', 'badge', 'is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('title',)
    list_filter = ('is_active', 'badge')


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            new_category_id = self.data.get('new_category')
            if new_category_id:
                try:
                    self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=new_category_id)
                except (ValueError, TypeError):
                    self.fields['subcategory'].queryset = SubCategory.objects.none()
            else:
                self.fields['subcategory'].queryset = SubCategory.objects.none()
        elif self.instance and self.instance.pk and self.instance.new_category:
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.new_category)
        else:
            self.fields['subcategory'].queryset = SubCategory.objects.none()
            
        self.fields['subcategory'].empty_label = "Select category first"


# 🔥 PRODUCT ADMIN (IMAGE + FILTER + BESTSELLER)
@admin.register(Product)
class ProductAdmin(NoDeleteAdmin):
    form = ProductForm

    def duplicate_products(self, request, queryset):
        for product in queryset:
            original_pk = product.pk
            # Fetch related sizes before losing the original PK
            original_sizes = list(ProductSize.objects.filter(product_id=original_pk))
            
            # Clone the product
            product.pk = None
            product.slug = ""  # Keep slug empty as requested
            
            # Save to create new instance
            # Note: The model's save() method will try to slugify the name.
            # If the name is identical, we might get an IntegrityError.
            # We'll try to save and if it fails, we'll append " (Copy)" to the name.
            try:
                product.save()
            except Exception:
                from django.utils.text import slugify
                import uuid
                product.name = f"{product.name} (Copy)"
                # Even with (Copy), slug might conflict if multiple copies exist.
                # We'll let Django try slugify again.
                product.slug = ""
                product.save()

            # Clone related sizes
            for size in original_sizes:
                size.pk = None
                size.product = product
                size.save()

        self.message_user(request, f"{queryset.count()} products duplicated successfully.")

    duplicate_products.short_description = "Duplicate selected products"

    def product_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:5px;" />',
                obj.image.url
            )
        return "-"

    product_image.short_description = "Image"
    product_image.admin_order_field = 'name'

    list_display = (
        'id',
        'product_image',
        'name',
        'price',
        'style_number',
        'stock',
        'is_bestseller',
        'is_featured',
        'is_active'
    )

    actions = ['duplicate_products']

    list_editable = (
        'price',
        'stock',
        'is_active',
        'is_bestseller',
        'is_featured'
    )

    search_fields = (
        'name',
        'style_number'
    )

    list_filter = (
        'material',
        'new_category',
        'is_active',
        'is_bestseller',
        'is_featured'
    )

    ordering = ('-id',)

    prepopulated_fields = {
        'slug': ('name',)
    }

    inlines = [ProductSizeInline]

    class Media:
        js = ('admin/js/chained-categories-v7.js',)

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'slug',
                'new_category',
                'subcategory',
                'price',
                'discount_price',
                'stock'
            )
        }),

        ('Product Media', {
            'fields': (
                'image',
                'detail_image_1',
                'detail_image_2',
                'detail_image_3',
                'detail_image_4',
                'detail_image_5',
                'detail_image_6',
                'detail_image_7',
                'detail_image_8',
                'detail_image_9',
                'video'
            )
        }),

        ('Product Specifications', {
            'fields': (
                'material',
                'type',
                'style_number',
                'silver_weight',
                'chain_length',
                'bracelet_size',
                'standard_preferable_chain_sizes'
            )
        }),

        ('Descriptions', {
            'fields': (
                'description',
                'product_details',
                'care_instructions',
                'activation_guidance',
                'size_chart'
            )
        }),

        ('Visibility', {
            'fields': (
                'is_bestseller',
                'is_featured',
                'is_active'
            )
        }),
    )


# 🔥 ORDER ITEM INLINE (ORDER DETAIL MA PRODUCT SHOW)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


# 🛒 ORDER ADMIN (TARO + IMPROVED)
@admin.register(Order)
class OrderAdmin(NoDeleteAdmin):
    def cancel_orders(self, request, queryset):
        queryset.update(status='Cancelled')
    cancel_orders.short_description = "Cancel selected orders"

    list_display = (
        'id',
        'name',
        'mobile',
        'total',
        'payment_method',
        'status',
        'is_paid',
        'created_at'
    )

    list_editable = (
        'status',
        'is_paid'
    )

    list_filter = (
        'status',
        'is_paid',
        'payment_method',
        'shipping_method',
        'created_at'
    )

    search_fields = (
        'name',
        'mobile',
        'email',
        'tracking_number'
    )

    ordering = ('-created_at',)

    date_hierarchy = 'created_at'

    inlines = [OrderItemInline]
    
    actions = ['cancel_orders']

    readonly_fields = (
        'razorpay_order_id',
        'razorpay_payment_id',
        'razorpay_signature',
        'created_at'
    )

# 🎁 COUPON ADMIN
@admin.register(Coupon)
class CouponAdmin(NoDeleteAdmin):
    list_display = ('code', 'discount_percentage', 'is_active', 'valid_from', 'valid_to')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('code',)

@admin.register(Wishlist)
class WishlistAdmin(NoDeleteAdmin):
    list_display = ('id', 'session_id', 'product', 'created_at')
    search_fields = ('session_id', 'product__name')


@admin.register(Cart)
class CartAdmin(NoDeleteAdmin):
    list_display = (
        'id',
        'session_id',
        'product',
        'quantity',
        'size',
        'created_at'
    )
    search_fields = ('session_id', 'product__name')


@admin.register(ContactMessage)
class ContactMessageAdmin(NoDeleteAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(HomepageSlider)
class HomepageSliderAdmin(NoDeleteAdmin):
    list_display = ('title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('title', 'text')
    list_filter = ('is_active',)
    ordering = ('display_order',)

    fieldsets = (
        (None, {
            'fields': ('title', 'is_active', 'display_order')
        }),
        ('Content', {
            'fields': ('slider_image', 'text', 'text_color', 'text_alignment')
        }),
        ('Button 1', {
            'fields': ('button_1_text', 'button_1_link', 'button_1_color')
        }),
        ('Button 2', {
            'fields': ('button_2_text', 'button_2_link', 'button_2_color')
        }),
    )

@admin.register(GoldSilverSection)
class GoldSilverSectionAdmin(NoDeleteAdmin):
    list_display = ('title', 'section_type', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    ordering = ('display_order',)

    fieldsets = (
        ('General', {
            'fields': ('section_type', 'title', 'title_suffix', 'image', 'is_active', 'display_order')
        }),
        ('Content', {
            'fields': ('subtitle', 'description', 'button_text', 'button_link')
        }),
        ('Styling', {
            'classes': ('collapse',),
            'fields': (
                'title_color', 'collection_color', 'text_color', 'line_color', 
                'button_bg_color', 'object_position'
            )
        }),
    )

class ComponentCardInline(admin.TabularInline):
    model = ComponentCard
    extra = 1
    ordering = ('display_order',)

@admin.register(ComponentsSection)
class ComponentsSectionAdmin(NoDeleteAdmin):
    list_display = ('title', 'subtitle_part_1', 'subtitle_part_2', 'is_active')
    list_editable = ('is_active',)
    inlines = [ComponentCardInline]

class OccasionCardInline(admin.TabularInline):
    model = OccasionCard
    extra = 1
    ordering = ('display_order',)

@admin.register(OccasionsSection)
class OccasionsSectionAdmin(NoDeleteAdmin):
    list_display = ('title', 'subtitle', 'is_active')
    list_editable = ('is_active',)
    inlines = [OccasionCardInline]

class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 1
    ordering = ('display_order',)

@admin.register(FAQSection)
class FAQSectionAdmin(NoDeleteAdmin):
    list_display = ('title', 'button_text', 'is_active')
    list_editable = ('is_active',)
    inlines = [FAQItemInline]

class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    ordering = ('display_order',)

@admin.register(TestimonialsSection)
class TestimonialsSectionAdmin(NoDeleteAdmin):
    list_display = ('title', 'subtitle', 'bottom_text', 'is_active')
    list_editable = ('is_active',)
    inlines = [TestimonialInline]

class FooterMenuItemInline(NestedTabularInline):
    model = FooterMenuItem
    extra = 1
    ordering = ('display_order',)

class FooterMenuInline(NestedStackedInline):
    model = FooterMenu
    extra = 1
    ordering = ('display_order',)
    inlines = [FooterMenuItemInline]

@admin.register(FooterMenu)
class FooterMenuAdmin(NoDeleteAdmin):
    list_display = ('title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    inlines = [FooterMenuItemInline]
    list_filter = ('is_active',)
    search_fields = ('title',)

class FooterIconInline(admin.TabularInline):
    model = FooterIcon
    extra = 1
    ordering = ('display_order',)


@admin.register(Footer)
class FooterAdmin(NoDeleteAdmin):
    list_display = ('section1_title', 'section1_subscription_box_title',)
    inlines = [FooterIconInline]

    fieldsets = (
        ('Section 1: Brand & Subscription', {
            'fields': ('section1_title', 'section1_description', 'section1_subscription_box_title', 'section1_subscription_box_description')
        }),
    )

    def has_add_permission(self, request):
        return not Footer.objects.exists()

@admin.register(FooterSecondSection)
class FooterSecondSectionAdmin(NoDeleteNestedAdmin):
    list_display = ('footer', 'copyright_text_1',)
    inlines = [FooterMenuInline]

    fieldsets = (
        ('Copyright Information', {
            'fields': ('copyright_text_1', 'copyright_text_2')
        }),
    )

    def has_add_permission(self, request):
        return not FooterSecondSection.objects.filter(footer__isnull=False).exists()

class AboutSectionInline(admin.StackedInline):
    model = AboutSection
    extra = 1
    ordering = ('display_order',)

@admin.register(AboutPage)
class AboutPageAdmin(NoDeleteAdmin):
    inlines = [AboutSectionInline]

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()

@admin.register(ContactPage)
class ContactPageAdmin(NoDeleteAdmin):
    def has_add_permission(self, request):
        return not ContactPage.objects.exists()

@admin.register(Policy)
class PolicyAdmin(NoDeleteAdmin):
    list_display = ('title', 'slug', 'last_updated', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')