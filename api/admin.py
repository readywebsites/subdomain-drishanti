from django.contrib import admin

from django.utils.html import format_html
from .models import Product, Order, OrderItem, Wishlist, Cart, Coupon, Category, SubCategory, ProductSize, CustomizedProduct, ContactMessage


# 📂 CATEGORY ADMIN
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'slug')
    search_fields = ('name',)
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CustomizedProduct)
class CustomizedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'badge', 'is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('title',)
    list_filter = ('is_active', 'badge')


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


# 🔥 PRODUCT ADMIN (IMAGE + FILTER + BESTSELLER)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

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
        'category',
        'is_active',
        'is_bestseller',
        'is_featured'
    )

    ordering = ('-id',)

    prepopulated_fields = {
        'slug': ('name',)
    }

    inlines = [ProductSizeInline]

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'slug',
                'new_category',
                'subcategory',
                'category',
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
                'video',
                'gallery_images'
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
class OrderAdmin(admin.ModelAdmin):

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

    readonly_fields = (
        'razorpay_order_id',
        'razorpay_payment_id',
        'razorpay_signature',
        'created_at'
    )


# 🔥 ORDER ITEM ADMIN (OPTIONAL VIEW)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('product__name',)


# 🎁 COUPON ADMIN
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'is_active', 'valid_from', 'valid_to')
    list_filter = ('is_active',)
    search_fields = ('code',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_id', 'product', 'created_at')
    search_fields = ('session_id', 'product__name')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
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
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
