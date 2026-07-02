import hmac
import hashlib
import razorpay
import random
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.db.models import Q
from .models import (
    Order, Product, Wishlist, Cart, Coupon, OrderItem, Category, 
    SubCategory, CustomizedProduct, ContactMessage, NewsletterSubscription,
    HomepageSlider, GoldSilverSection, ComponentsSection, OccasionsSection,
    FAQSection, TestimonialsSection, Footer, AboutPage, ContactPage, Policy,
    UserProfile, OTPVerification
)
from .serializers import (
    ProductSerializer, WishlistSerializer, CartSerializer, 
    OrderSerializer, CategorySerializer, SubCategorySerializer,
    CustomizedProductSerializer, ContactMessageSerializer, 
    NewsletterSubscriptionSerializer, HomepageSliderSerializer,
    GoldSilverSectionSerializer, ComponentsSectionSerializer, OccasionsSectionSerializer,
    FAQSectionSerializer, TestimonialsSectionSerializer, FooterSerializer,
    AboutPageSerializer, ContactPageSerializer, PolicySerializer
)


from rest_framework.generics import ListAPIView, RetrieveAPIView # Added RetrieveAPIView
from django.shortcuts import render

class HomepageSliderView(ListAPIView):
    queryset = HomepageSlider.objects.filter(is_active=True).order_by('display_order')
    serializer_class = HomepageSliderSerializer
    permission_classes = [AllowAny]

class NewsletterSubscriptionView(APIView):

    def post(self, request):
        print("NEWSLETTER HIT")
        print(request.data)

        serializer = NewsletterSubscriptionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            print("SAVED SUCCESSFULLY")

            return Response(
                {"message": "Subscribed successfully"},
                status=status.HTTP_201_CREATED
            )

        print("VALIDATION ERRORS:", serializer.errors)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
def frontend(request):
    return render(request, "index.html")

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_customized_products(request):
    products = CustomizedProduct.objects.filter(is_active=True).order_by('-created_at')
    serializer = CustomizedProductSerializer(products, many=True)
    return Response(serializer.data)

# 📂 CATEGORY VIEWS
class CategoryListView(ListAPIView):
    queryset = Category.objects.prefetch_related('subcategories')
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
            Q(description__icontains=search) |
            Q(style_number__icontains=search)
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_razorpay_order(request):
    amount = int(request.data.get('amount', 0)) * 100
    if amount <= 0:
        return Response({'detail': 'Invalid amount'}, status=400)

    try:
        if not settings.RAZORPAY_KEY_ID or settings.RAZORPAY_KEY_ID == 'your_key_id':
            return Response({'detail': 'Razorpay Key ID is not configured in the .env file.'}, status=400)
        if not settings.RAZORPAY_KEY_SECRET or settings.RAZORPAY_KEY_SECRET == 'your_key_secret':
            return Response({'detail': 'Razorpay Key Secret is not configured in the .env file.'}, status=400)

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
    except Exception as e:
        return Response({
            'detail': f'Razorpay SDK Error: {str(e)}',
            'info': 'Please check if your Razorpay Key ID and Secret Key in subdomain-backend/.env are correct.'
        }, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
        email=request.user.email,
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
        email=request.user.email,
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
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def get_user_orders(request):
    orders = Order.objects.none()
    if request.user and request.user.is_authenticated:
        orders = Order.objects.filter(email=request.user.email)
    else:
        session_id = request.headers.get('X-Session-ID') or request.GET.get('session_id')
        mobile = request.GET.get('mobile')
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
        size = request.data.get('size', 'Standard') or 'Standard'
        
        # Check if the product already exists in the cart for this session (ignoring size variation)
        item = Cart.objects.filter(session_id=session_id, product_id=product_id).first()
        if item:
            item.quantity += quantity
            item.save()
        else:
            item = Cart.objects.create(
                session_id=session_id,
                product_id=product_id,
                size=size,
                quantity=quantity
            )
            
        return Response(CartSerializer(item).data)

    if request.method == 'PATCH':
        product_id = request.data.get('product_id')
        size = request.data.get('size')
        quantity = int(request.data.get('quantity'))
        
        # Try to find by both product_id and size, fallback to product_id if not found
        item = None
        if size:
            item = Cart.objects.filter(session_id=session_id, product_id=product_id, size=size).first()
        if not item:
            item = Cart.objects.filter(session_id=session_id, product_id=product_id).first()
            
        if item:
            item.quantity = quantity
            item.save()
            return Response(CartSerializer(item).data)
        return Response({'detail': 'Cart item not found'}, status=404)

    if request.method == 'DELETE':
        product_id = request.data.get('product_id')
        size = request.data.get('size')
        
        deleted = False
        if size:
            deleted_count, _ = Cart.objects.filter(session_id=session_id, product_id=product_id, size=size).delete()
            if deleted_count > 0:
                deleted = True
        if not deleted:
            Cart.objects.filter(session_id=session_id, product_id=product_id).delete()
            
        return Response({'status': 'deleted'})


# 📩 CONTACT FORM SUBMISSION VIEW
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def contact_view(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'message': 'Message saved successfully!'}, status=201)
    return Response(serializer.errors, status=400)

class GoldSilverSectionView(ListAPIView):
    queryset = GoldSilverSection.objects.filter(is_active=True).order_by('display_order')
    serializer_class = GoldSilverSectionSerializer
    permission_classes = [AllowAny]

class ComponentsSectionView(ListAPIView):
    queryset = ComponentsSection.objects.all()
    serializer_class = ComponentsSectionSerializer
    permission_classes = [AllowAny]

class OccasionsSectionView(ListAPIView):
    queryset = OccasionsSection.objects.all()
    serializer_class = OccasionsSectionSerializer
    permission_classes = [AllowAny]

class FAQSectionView(ListAPIView):
    queryset = FAQSection.objects.all()
    serializer_class = FAQSectionSerializer
    permission_classes = [AllowAny]

class TestimonialsSectionView(ListAPIView):
    queryset = TestimonialsSection.objects.all()
    serializer_class = TestimonialsSectionSerializer
    permission_classes = [AllowAny]

class FooterView(RetrieveAPIView):
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        footer_instance = Footer.objects.first()
        if not footer_instance:
            print("DEBUG: No Footer instance found in the database.")
        else:
            print(f"DEBUG: Footer instance found: {footer_instance.section1_title}")
        return footer_instance

class AboutPageView(RetrieveAPIView):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return AboutPage.objects.first()

class ContactPageView(RetrieveAPIView):
    queryset = ContactPage.objects.all()
    serializer_class = ContactPageSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return ContactPage.objects.first()

class PolicyListView(ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [AllowAny]

class PolicyDetailView(RetrieveAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


# 👤 AUTH & OTP VIEWS

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get('email', '').strip().lower()
    flow = request.data.get('flow', 'signup') # 'signup' or 'signin'

    if not email:
        return Response({'detail': 'Email is required.'}, status=400)

    # If signin, check if user exists
    if flow == 'signin':
        if not User.objects.filter(email=email).exists():
            return Response({'detail': 'This user does not exist, please signup'}, status=400)

    # Generate 6-digit OTP
    otp = f"{random.randint(100000, 999999)}"

    # Save to OTPVerification model
    OTPVerification.objects.create(email=email, otp=otp)

    # Print to console for easy testing
    print(f"\n======================================")
    print(f"OTP FOR {email}: {otp} (Flow: {flow})")
    print(f"======================================\n")

    # Send email
    subject = "Verify your email - Drishanti"
    message = f"Namaste,\n\nYour verification code is {otp}.\n\nThis code is valid for 10 minutes.\n\nWarm Regards,\nDrishanti Team"
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@drishanti.com',
            [email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

    return Response({'detail': 'OTP sent successfully.'})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get('email', '').strip().lower()
    otp = request.data.get('otp', '').strip()
    flow = request.data.get('flow', 'signup')

    if not email or not otp:
        return Response({'detail': 'Email and OTP are required.'}, status=400)

    # Find the latest OTP verification entry
    verification = OTPVerification.objects.filter(email=email, otp=otp, is_verified=False).order_by('-created_at').first()

    if not verification:
        return Response({'detail': 'Invalid or expired OTP.'}, status=400)

    # Check expiry (10 minutes)
    if timezone.now() - verification.created_at > timedelta(minutes=10):
        return Response({'detail': 'OTP has expired.'}, status=400)

    # Mark as verified
    verification.is_verified = True
    verification.save()

    # Get or create user
    user = None
    if flow == 'signup':
        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            # Username must be unique, we can use email as username
            user = User.objects.create_user(username=email, email=email)
            UserProfile.objects.get_or_create(user=user)
        else:
            user = User.objects.get(email=email)
            UserProfile.objects.get_or_create(user=user)
    else: # signin
        try:
            user = User.objects.get(email=email)
            UserProfile.objects.get_or_create(user=user)
        except User.DoesNotExist:
            return Response({'detail': 'User not found. Please signup.'}, status=400)

    # Generate token
    token, _ = Token.objects.get_or_create(user=user)

    # Migrate guest cart/wishlist to user account
    guest_session_id = request.data.get('session_id')
    if guest_session_id:
        user_session_id = f"user_{email}"
        # Merge cart items
        for cart_item in Cart.objects.filter(session_id=guest_session_id):
            user_item = Cart.objects.filter(session_id=user_session_id, product=cart_item.product).first()
            if user_item:
                user_item.quantity += cart_item.quantity
                user_item.save()
                cart_item.delete()
            else:
                cart_item.session_id = user_session_id
                cart_item.save()
        
        # Merge wishlist items
        for wishlist_item in Wishlist.objects.filter(session_id=guest_session_id):
            if Wishlist.objects.filter(session_id=user_session_id, product=wishlist_item.product).exists():
                wishlist_item.delete()
            else:
                wishlist_item.session_id = user_session_id
                wishlist_item.save()

    return Response({
        'token': token.key,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })


@api_view(['GET', 'PUT', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'GET':
        return Response({
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'mobile': profile.mobile,
            'address': profile.address,
            'city': profile.city,
            'state': profile.state,
            'pincode': profile.pincode,
            'country': profile.country,
        })

    elif request.method in ['PUT', 'PATCH']:
        data = request.data
        
        # Update User fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        user.save()

        # Update Profile fields
        profile.mobile = data.get('mobile', profile.mobile)
        profile.address = data.get('address', profile.address)
        profile.city = data.get('city', profile.city)
        profile.state = data.get('state', profile.state)
        profile.pincode = data.get('pincode', profile.pincode)
        profile.country = data.get('country', profile.country)
        profile.save()

        return Response({
            'detail': 'Profile updated successfully.',
            'profile': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'mobile': profile.mobile,
                'address': profile.address,
                'city': profile.city,
                'state': profile.state,
                'pincode': profile.pincode,
                'country': profile.country,
            }
        })