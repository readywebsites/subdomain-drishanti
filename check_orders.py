import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Order, OrderItem
from api.serializers import OrderSerializer

print("--- Order Data Check ---")
orders = Order.objects.all().order_by('-created_at')[:5]
for o in orders:
    print(f"Order ID: {o.id}, Total: {o.total}")
    serializer = OrderSerializer(o)
    import json
    # Print a clean representation of serialized items
    items_data = serializer.data.get('items', [])
    for item in items_data:
        print(f"  Item ID: {item.get('id')}")
        print(f"    Product: {item.get('product')}")
        print(f"    Product Details: {item.get('product_details')}")
    print("-" * 30)
