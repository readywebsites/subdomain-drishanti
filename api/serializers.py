from rest_framework import serializers
from .models import Category, SubCategory, Product, Coupon, Order, OrderItem, Wishlist, Cart

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'subcategories']

class ProductSerializer(serializers.ModelSerializer):
    new_category_name = serializers.CharField(source='new_category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    coupon_code = serializers.CharField(source='coupon.code', read_only=True)

    class Meta:
        model = Order
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
        fields = ['id', 'session_id', 'product', 'product_name', 'product_image', 'product_price', 'product_discount_price', 'quantity', 'size', 'created_at']