from django.contrib import admin
from .models import Product, Order, OrderItem, Wishlist, Cart, Coupon, Category, SubCategory


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


# 🔥 PRODUCT ADMIN (IMAGE + FILTER + BESTSELLER)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)


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
