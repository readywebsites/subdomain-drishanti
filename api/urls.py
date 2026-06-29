from django.urls import path
from .views import (
    create_razorpay_order, verify_payment, get_products, get_bestsellers, 
    get_featured, get_product_detail, wishlist_manager, cart_manager, 
    clear_cart, apply_coupon, create_cod_order, get_user_orders, get_order_detail,
    CategoryListView, SubCategoryListView, get_customized_products, contact_view, 
    NewsletterSubscriptionView, HomepageSliderView, GoldSilverSectionView,
    ComponentsSectionView, OccasionsSectionView, FAQSectionView, TestimonialsSectionView,
    FooterView, AboutPageView, ContactPageView, PolicyListView, PolicyDetailView
)

urlpatterns = [
    path('homepage-slider/', HomepageSliderView.as_view()),
    path('goldsilver-sections/', GoldSilverSectionView.as_view()),
    path('components-section/', ComponentsSectionView.as_view()),
    path('occasions-section/', OccasionsSectionView.as_view()),
    path('faq-section/', FAQSectionView.as_view()),
    path('testimonials-section/', TestimonialsSectionView.as_view()),
    path('footer/', FooterView.as_view()),
    path('about-page/', AboutPageView.as_view()),
    path('contact-page/', ContactPageView.as_view()),
    path('policies/', PolicyListView.as_view()),
    path('policies/<slug:slug>/', PolicyDetailView.as_view()),
    path('products/', get_products),
    path('customized-products/', get_customized_products),
    path('products/bestsellers/', get_bestsellers),
    path('products/featured/', get_featured),
    path('products/<slug:slug>/', get_product_detail),
    
    path('categories/', CategoryListView.as_view()),
    path('subcategories/', SubCategoryListView.as_view()),
    
    path('wishlist/', wishlist_manager),
    path('cart/', cart_manager),
    path('cart/clear/', clear_cart),
    path('coupons/apply/', apply_coupon),
    path('create-order/', create_razorpay_order),
    path('create-cod-order/', create_cod_order),
    path('verify-payment/', verify_payment),
    path('orders/', get_user_orders),
    path('orders/<int:pk>/', get_order_detail),
    path('contact/', contact_view),
    path("newsletter/subscribe/",NewsletterSubscriptionView.as_view(),name="newsletter-subscribe"),
]