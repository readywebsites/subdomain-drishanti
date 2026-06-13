from django.contrib import admin
from .models import Product, Order, OrderItem, Wishlist, Cart, Coupon, Category, SubCategory, ProductSize


# 📂 CATEGORY ADMIN
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1


# 🔥 PRODUCT ADMIN (IMAGE + FILTER + BESTSELLER)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'style_number', 'silver_weight', 'stock', 'is_active')
    list_editable = ('price', 'stock', 'is_active')
    search_fields = ('name', 'style_number')
    list_filter = ('material', 'category', 'is_active', 'is_bestseller', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'new_category', 'subcategory', 'category', 'price', 'discount_price', 'stock')
        }),
        ('Product Media', {
            'fields': (
                'image', 
                'detail_image_1', 'detail_image_2', 'detail_image_3', 
                'detail_image_4', 'detail_image_5', 'detail_image_6', 
                'detail_image_7', 'detail_image_8', 'detail_image_9',
                'video',
                'gallery_images'
            )
        }),
        ('Product Specifications', {
            'fields': ('material', 'type', 'style_number', 'silver_weight', 'chain_length', 'bracelet_size', 'standard_preferable_chain_sizes')
        }),
        ('Descriptions & Guidance', {
            'fields': ('description', 'product_details', 'care_instructions', 'activation_guidance', 'size_chart')
        }),
        ('Status & Visibility', {
            'fields': ('is_bestseller', 'is_featured', 'is_active')
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
        'razorpay_order_id',
        'razorpay_payment_id',
        'tracking_number'
    )

    inlines = [OrderItemInline]

    readonly_fields = (
        'razorpay_order_id',
        'razorpay_payment_id',
        'razorpay_signature',
        'created_at'
    )

    ordering = ('-created_at',)

    list_editable = ('status', 'is_paid')


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

admin.site.register(Wishlist)
admin.site.register(Cart)
