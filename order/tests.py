from django.test import TestCase
from django.contrib.auth.models import User
from product.models import Product, Category
from .models import OrderRequest, OrderRequestItem, PaymentSchedule
from decimal import Decimal

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            price=1000.00,
            category=self.category
        )

    def test_order_request_creation(self):
        order = OrderRequest.objects.create(
            user=self.user,
            total_price=1000.00,
            down_payment=100.00,
            installment_duration_months=12
        )
        self.assertEqual(order.status, 'IN_PROGRESS')
        self.assertEqual(str(order), f"OrderRequest {order.id} by {self.user.username}")

    def test_order_item_subtotal_signal(self):
        order = OrderRequest.objects.create(
            user=self.user,
            total_price=2000.00,
            down_payment=200.00,
            installment_duration_months=12
        )
        item = OrderRequestItem.objects.create(
            order_request=order,
            product=self.product,
            quantity=2,
            price_at_time=self.product.price
        )
        # Signal should calculate subtotal: 2 * 1000 = 2000
        self.assertEqual(item.subtotal, Decimal('2000.00'))

    def test_payment_schedule_creation(self):
        order = OrderRequest.objects.create(
            user=self.user,
            total_price=1000.00,
            down_payment=100.00,
            installment_duration_months=12
        )
        schedule = PaymentSchedule.objects.create(
            order_request=order,
            due_date='2025-01-01',
            amount=75.00
        )
        self.assertEqual(schedule.status, 'UPCOMING')
