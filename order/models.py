from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django.db.models.signals import pre_save
from django.dispatch import receiver
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
    admin_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"OrderRequest {self.id} by {self.user.username}"


class OrderRequestItem(models.Model):
    order_request = models.ForeignKey(OrderRequest, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2, null=True) # Price when the order was made
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # quantity * price_at_time

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for OrderRequest {self.order_request.id}"


@receiver(pre_save, sender=OrderRequestItem)
def set_subtotal(sender, instance, **kwargs):
    instance.subtotal = instance.quantity * instance.price_at_time


class PaymentSchedule(models.Model):
    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('UPCOMING', 'Upcoming'),
        ('PENDING', 'Pending'), # Or 'OVERDUE'
    ]

    order_request = models.ForeignKey(OrderRequest, related_name='payment_schedules', on_delete=models.CASCADE)
    due_date = models.DateField() # When the payment is due
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPCOMING')
    payment_date = models.DateTimeField(null=True, blank=True) # Dwhen payment should be done.
    
    def __str__(self):
        return f"Installment for Order #{self.order_request.id} due on {self.due_date}"