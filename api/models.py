from django.db import models


# 📂 CATEGORY MODELS
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

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
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    image = models.ImageField(upload_to='products/')
    gallery_images = models.JSONField(default=list, blank=True, help_text="List of additional product image URLs")
    description = models.TextField(blank=True)

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


# 🎁 COUPON MODEL
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code


# 🛒 ORDER MODEL
class Order(models.Model):
    PAYMENT_CHOICES = (
        ('Razorpay', 'Razorpay'),
        ('COD', 'Cash on Delivery'),
    )
    
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    SHIPPING_CHOICES = (
        ('Standard', 'Standard Shipping'),
        ('Express', 'Express Shipping'),
    )

    session_id = models.CharField(max_length=100, db_index=True, blank=True, null=True)

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15)

    # Shipping Address
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')

    # Billing Address
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

    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} — {self.name}"


# 🔥 ORDER ITEMS
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)
    price = models.IntegerField()  # snapshot price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# 💖 WISHLIST MODEL
class Wishlist(models.Model):
    session_id = models.CharField(max_length=100, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_id', 'product')

    def __str__(self):
        return f"{self.session_id} - {self.product.name}"


# 🛒 CART MODEL
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
