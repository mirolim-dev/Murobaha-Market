# orders/views.py

from django.db import transaction # For atomic operations
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import OrderRequest, PaymentSchedule
from .serializers import (
    CreateOrderRequestSerializer,
    OrderRequestListSerializer,
    OrderRequestDetailSerializer,
    PaymentScheduleSerializer
)

# from cart.models import Cart, CartItem 

class OrderRequestListCreateView(generics.ListCreateAPIView):
    """
    - GET: Lists all order requests for the authenticated user.
    - POST: Creates a new order request from the user's current cart.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderRequestSerializer
        return OrderRequestListSerializer

    def get_queryset(self):
        # Only return order requests belonging to the currently logged-in user
        return OrderRequest.objects.filter(user=self.request.user).order_by('-request_sent_time')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Use a database transaction to ensure all or nothing is saved
        with transaction.atomic():
            cart = request.user.cart
            cart_items = cart.items.all()
            
            # Calculate total price from cart items
            total_price = sum(item.product.price * item.quantity for item in cart_items)

            # Create the OrderRequest instance
            order_request = OrderRequest.objects.create(
                user=request.user,
                total_price=total_price,
                **serializer.validated_data
            )

            # Create OrderRequestItem instances for each item in the cart
            order_items_to_create = [
                OrderRequestItem(
                    order_request=order_request,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_time_of_order=item.product.price
                ) for item in cart_items
            ]
            OrderRequestItem.objects.bulk_create(order_items_to_create)

            # Clear the user's cart
            cart_items.delete()

        # Return the newly created order's full detail
        response_serializer = OrderRequestDetailSerializer(order_request)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderRequestDetailView(generics.RetrieveAPIView):
    """
    - GET: Retrieves the details of a specific order request.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderRequestDetailSerializer
    
    def get_queryset(self):
        # Ensure users can only view their own order requests
        return OrderRequest.objects.filter(user=self.request.user)
    

class PaymentScheduleDetailView(generics.RetrieveAPIView):
    """
    - GET: Retrieves the details of a specific payment schedule.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentScheduleSerializer
    
    def get_queryset(self, order_request_id:int):
        # Ensure users can only view payment schedules for their own orders
        return PaymentSchedule.objects.get(order_request__id=order_request_id)
    