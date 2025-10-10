# orders/serializers.py

from rest_framework import serializers
from product.serializers import ProductSerializer # To display product details
from .models import OrderRequest, OrderRequestItem, PaymentSchedule

# --- Serializers for Reading/Displaying Data ---

class OrderRequestItemSerializer(serializers.ModelSerializer):
    """Serializer for items within an order request."""
    # Nest the ProductSerializer to show full product details for each item
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderRequestItem
        fields = ['id', 'product', 'quantity', 'price_at_time']


class PaymentScheduleSerializer(serializers.ModelSerializer):
    """Serializer for viewing payment schedules."""
    class Meta:
        model = PaymentSchedule
        fields = ['id', 'due_date', 'amount', 'status', 'payment_date']


# class CreatePaymentScheduleSerializer(serializers.ModelSerializer):
#     """Serializer for creating payment schedules."""
#     class Meta:
#         model = PaymentSchedule
#         fields = ['due_date', 'amount', 'status', 'payment_date']

#     def validate_amount(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Payment amount must be positive.")
#         return value
    
#     def validate_due_date(self, value):
#         from datetime import date, timedelta
#         min_due_date = date.today() + timedelta(days=6*30)  # Approximate 6 months as 180 days
#         if value < min_due_date:
#             raise serializers.ValidationError("Due date should be at least 6 months from today.")
#         return value


class OrderRequestListSerializer(serializers.ModelSerializer):
    """
    A lightweight serializer for listing all of a user's order requests.
    (Matches the "My Requests" screen).
    """
    class Meta:
        model = OrderRequest
        fields = ['id', 'status', 'total_price', 'request_sent_time']


class OrderRequestDetailSerializer(serializers.ModelSerializer):
    """
    A detailed serializer for a single order request.
    Includes all items and the payment schedule if available.
    """
    items = OrderRequestItemSerializer(many=True, read_only=True)
    payment_schedules = PaymentScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = OrderRequest
        fields = [
            'id', 'status', 'total_price', 'down_payment',
            'installment_duration_months', 'request_sent_time', 'admin_notes',
            'items', 'payment_schedules'
        ]


# --- Serializer for Creating Data ---

class CreateOrderRequestSerializer(serializers.ModelSerializer):
    """
    Serializer used specifically for CREATING a new order request.
    Takes a down payment and duration, and validates the request.
    """
    class Meta:
        model = OrderRequest
        fields = ['down_payment', 'installment_duration_months']
        # The other fields (user, total_price, status, items) will be set in the view's logic.

    def validate(self, attrs):
        # You can add validation logic here. For example:
        if attrs['installment_duration_months'] not in [6, 9, 12, 18, 24]:
            raise serializers.ValidationError("Invalid installment duration.")
        
        # Ensure the user's cart is not empty
        cart = self.context['request'].user.cart # We will pass the request context to the serializer
        if not cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")
            
        return attrs