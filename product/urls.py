# products/urls.py (NO CHANGES NEEDED)

from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView
)

app_name = 'products'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]