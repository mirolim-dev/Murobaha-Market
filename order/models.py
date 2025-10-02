from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.

class OrderRequest(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('ACCEPTED', 'Accepted'),
        ('DENIED', 'Denied'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, related_name='order_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    installment_duration_months = models.IntegerField()
    request_sent_time = models.DateTimeField(auto_now_add=True)
    # Additional fields like admin notes for denial/acceptance can be added

class OrderRequestItem(models.Model):
    order_request = models.ForeignKey(OrderRequest, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class PaymentSchedule(models.Model):
    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('UPCOMING', 'Upcoming'),
        ('PENDING', 'Pending'), # Or 'OVERDUE'
    ]

    order_request = models.ForeignKey(OrderRequest, related_name='payment_schedules', on_delete=models.CASCADE)
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPCOMING')
    payment_date = models.DateTimeField(null=True, blank=True) # Date when payment was made