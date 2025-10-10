from django.urls import path

from .views import (
    OrderRequestListCreateView,
    OrderRequestDetailView,
    PaymentScheduleDetailView
)

urlpatterns = [
    path('', OrderRequestListCreateView.as_view(), name='order-request-list-create'),
    path('<int:pk>/', OrderRequestDetailView.as_view(), name='order-request-detail'),
    path('payment-schedule/<int:pk>/', PaymentScheduleDetailView.as_view(), name='payment-schedule-detail'),
]