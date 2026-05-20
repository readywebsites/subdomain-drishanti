import hmac
import hashlib
import razorpay
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from .models import Order, Product, Wishlist, Cart, Coupon, OrderItem, Category, SubCategory
from .serializers import (
    ProductSerializer, WishlistSerializer, CartSerializer, 
    OrderSerializer, CategorySerializer, SubCategorySerializer
)


from rest_framework.generics import ListAPIView
from django.shortcuts import render

def frontend(request):
    return render(request, "index.html")

# 📂 CATEGORY VIEWS
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class SubCategoryListView(ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_products(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    # New Model Filters
    category_slug = request.GET.get('category')
    subcategory_slug = request.GET.get('subcategory')
    
    # Legacy Filters (kept for compatibility)
    material = request.GET.get('material')
    ptype = request.GET.get('type')
    search = request.GET.get('search')

    if category_slug:
        products = products.filter(new_category__slug=category_slug)
    if subcategory_slug:
        products = products.filter(subcategory__slug=subcategory_slug)
        
    if material:
        products = products.filter(material__iexact=material)
    if ptype:
        products = products.filter(type__iexact=ptype)
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_bestsellers(request):
    products = Product.objects.filter(is_active=True, is_bestseller=True).order_by('-created_at')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_featured(request):
    products = Product.objects.filter(is_active=True, is_featured=True).order_by('-created_at')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug, is_active=True)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=404)


# 🎟️ COUPONS
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def apply_coupon(request):
    code = request.data.get('code')
    if not code:
        return Response({'detail': 'Coupon code required.'}, status=400)
        
    try:
        coupon = Coupon.objects.get(code__iexact=code, is_active=True)
        now = timezone.now()
        if coupon.valid_from and now < coupon.valid_from:
            return Response({'detail': 'Coupon is not valid yet.'}, status=400)
        if coupon.valid_to and now > coupon.valid_to:
            return Response({'detail': 'Coupon has expired.'}, status=400)
        
        return Response({
            'code': coupon.code,
            'discount_percentage': coupon.discount_percentage
        })
    except Coupon.DoesNotExist:
        return Response({'detail': 'Invalid coupon code.'}, status=400)


# 🚚 CHECKOUT HELPERS
def _create_order_items(order, session_id):
    cart_items = Cart.objects.filter(session_id=session_id)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.discount_price if item.product.discount_price else item.product.price
        )

def _get_delivery_estimate(shipping_method):
    if shipping_method == 'Express':
        return timezone.now().date() + timedelta(days=2)
    return timezone.now().date() + timedelta(days=5)

def _send_order_email(order):
    if not order.email:
        return
    subject = f"Order Confirmation - {order.id}"
    message = f"Namaste {order.name},\n\nYour order #{order.id} has been placed successfully.\nTotal Amount: Rs. {order.total}\nPayment Method: {order.payment_method}\n\nWe will notify you once it ships.\n\nWarm Regards,\nDrishanti Team"
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@drishanti.com',
            [order.email],
            fail_silently=True,
        )
    except Exception as e:
        pass


# 💳 PAYMENTS & ORDERS
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def create_razorpay_order(request):
    amount = int(request.data.get('amount', 0)) * 100
    if amount <= 0:
        return Response({'detail': 'Invalid amount'}, status=400)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': 1,
    })

    return Response({
        'order_id': payment['id'],
        'amount': payment['amount'],
        'currency': payment['currency'],
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def verify_payment(request):
    data = request.data
    
    generated_signature = hmac.new(
        bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
        bytes(f"{data.get('razorpay_order_id')}|{data.get('razorpay_payment_id')}", 'utf-8'),
        hashlib.sha256
    ).hexdigest()

    if generated_signature != data.get('razorpay_signature'):
        return Response({'status': 'failed', 'detail': 'Signature verification failed'}, status=400)

    coupon_obj = None
    if data.get('coupon_code'):
        try:
            coupon_obj = Coupon.objects.get(code__iexact=data['coupon_code'], is_active=True)
        except Coupon.DoesNotExist:
            pass

    order = Order.objects.create(
        session_id=data.get('session_id'),
        name=data.get('name'),
        email=data.get('email'),
        mobile=data.get('mobile'),
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        pincode=data.get('pincode'),
        billing_address=data.get('billing_address'),
        billing_city=data.get('billing_city'),
        billing_pincode=data.get('billing_pincode'),
        subtotal=int(data.get('subtotal', 0)),
        tax=int(data.get('tax', 0)),
        shipping_charge=int(data.get('shipping_charge', 0)),
        coupon=coupon_obj,
        discount=int(data.get('discount', 0)),
        total=int(data.get('total', 0)),
        payment_method='Razorpay',
        shipping_method=data.get('shipping_method', 'Standard'),
        status='Processing',
        razorpay_order_id=data.get('razorpay_order_id'),
        razorpay_payment_id=data.get('razorpay_payment_id'),
        razorpay_signature=data.get('razorpay_signature'),
        is_paid=True,
        delivery_estimate=_get_delivery_estimate(data.get('shipping_method', 'Standard'))
    )

    if data.get('session_id'):
        _create_order_items(order, data.get('session_id'))
        Cart.objects.filter(session_id=data.get('session_id')).delete()

    _send_order_email(order)

    return Response({'status': 'success', 'order_id': order.id})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def create_cod_order(request):
    data = request.data
    
    coupon_obj = None
    if data.get('coupon_code'):
        try:
            coupon_obj = Coupon.objects.get(code__iexact=data['coupon_code'], is_active=True)
        except Coupon.DoesNotExist:
            pass

    order = Order.objects.create(
        session_id=data.get('session_id'),
        name=data.get('name'),
        email=data.get('email'),
        mobile=data.get('mobile'),
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        pincode=data.get('pincode'),
        billing_address=data.get('billing_address'),
        billing_city=data.get('billing_city'),
        billing_pincode=data.get('billing_pincode'),
        subtotal=int(data.get('subtotal', 0)),
        tax=int(data.get('tax', 0)),
        shipping_charge=int(data.get('shipping_charge', 0)),
        coupon=coupon_obj,
        discount=int(data.get('discount', 0)),
        total=int(data.get('total', 0)),
        payment_method='COD',
        shipping_method=data.get('shipping_method', 'Standard'),
        status='Processing',
        is_paid=False,
        delivery_estimate=_get_delivery_estimate(data.get('shipping_method', 'Standard'))
    )

    if data.get('session_id'):
        _create_order_items(order, data.get('session_id'))
        Cart.objects.filter(session_id=data.get('session_id')).delete()

    _send_order_email(order)

    return Response({'status': 'success', 'order_id': order.id})


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_user_orders(request):
    session_id = request.headers.get('X-Session-ID') or request.GET.get('session_id')
    mobile = request.GET.get('mobile')
    
    orders = Order.objects.none()
    if session_id:
        orders = Order.objects.filter(session_id=session_id)
    elif mobile:
        orders = Order.objects.filter(mobile=mobile)
        
    orders = orders.order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found'}, status=404)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def clear_cart(request):
    session_id = (
        request.headers.get('X-Session-ID') or 
        request.data.get('session_id') or 
        request.GET.get('session_id')
    )
    if not session_id:
        return Response({'detail': 'Session ID required'}, status=400)
    Cart.objects.filter(session_id=session_id).delete()
    return Response({'status': 'cart cleared'})


# 💖 WISHLIST VIEWS

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def wishlist_manager(request):

    session_id = (
        request.headers.get('X-Session-ID') or 
        request.GET.get('session_id') or 
        request.data.get('session_id')
    )

    if not session_id:
        return Response(
            {'detail': 'Session ID required'},
            status=400
        )

    # GET WISHLIST
    if request.method == 'GET':
        items = Wishlist.objects.filter(session_id=session_id)
        serializer = WishlistSerializer(items, many=True)
        return Response(serializer.data)

    # ADD / REMOVE WISHLIST
    elif request.method == 'POST':

        try:
            product_id = request.data.get('product_id')

            if not product_id:
                return Response(
                    {'detail': 'Product ID required'},
                    status=400
                )

            product = Product.objects.get(id=product_id)

            item, created = Wishlist.objects.get_or_create(
                session_id=session_id,
                product=product
            )

            # REMOVE IF ALREADY EXISTS
            if not created:
                item.delete()
                return Response({'status': 'removed'})

            # ADD NEW
            serializer = WishlistSerializer(item)

            return Response(
                serializer.data,
                status=201
            )

        except Product.DoesNotExist:
            return Response(
                {'detail': 'Product not found'},
                status=404
            )

        except Exception as e:
            print("WISHLIST ERROR:", str(e))

            return Response(
                {'detail': str(e)},
                status=500
            )

    # DELETE ITEM
    elif request.method == 'DELETE':

        product_id = request.data.get('product_id')

        if not product_id:
            return Response(
                {'detail': 'Product ID required'},
                status=400
            )

        Wishlist.objects.filter(
            session_id=session_id,
            product_id=product_id
        ).delete()

        return Response({'status': 'deleted'})

# 🛒 CART VIEWS
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def cart_manager(request):
    session_id = (
        request.headers.get('X-Session-ID') or 
        request.GET.get('session_id') or 
        request.data.get('session_id')
    )
    if not session_id:
        return Response({'detail': 'Session ID required'}, status=400)

    if request.method == 'GET':
        items = Cart.objects.filter(session_id=session_id)
        serializer = CartSerializer(items, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        size = request.data.get('size', 'Standard')
        
        item, created = Cart.objects.get_or_create(
            session_id=session_id, 
            product_id=product_id, 
            size=size,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
            
        return Response(CartSerializer(item).data)

    if request.method == 'PATCH':
        product_id = request.data.get('product_id')
        size = request.data.get('size', 'Standard')
        quantity = int(request.data.get('quantity'))
        
        item = Cart.objects.get(session_id=session_id, product_id=product_id, size=size)
        item.quantity = quantity
        item.save()
        return Response(CartSerializer(item).data)

    if request.method == 'DELETE':
        product_id = request.data.get('product_id')
        size = request.data.get('size', 'Standard')
        Cart.objects.filter(session_id=session_id, product_id=product_id, size=size).delete()
        return Response({'status': 'deleted'})
