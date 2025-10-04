
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer

# --- Category Views ---

class CategoryListView(generics.ListAPIView):
    """
    API view to list all product categories.
    Anyone can access this endpoint.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny] # Publicly accessible


# --- Product Views ---

class ProductListView(generics.ListAPIView):
    """
    API view to list all products.
    Supports searching, filtering, and ordering.
    Anyone can access this endpoint.
    """
    queryset = Product.objects.all().select_related('category') # .select_related('category') is a performance optimization
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny] # Publicly accessible

    # --- Powerful Filtering and Searching ---
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # 1. DjangoFilterBackend: For filtering by specific field values
    filterset_fields = ['category', 'category__name'] # Allow filtering like /api/products/?category=1
    
    # 2. SearchFilter: For full-text search
    search_fields = ['name', 'description'] # Allow searching like /api/products/?search=jacket
    
    # 3. OrderingFilter: For sorting the results
    ordering_fields = ['price', 'name', 'created_at'] # Allow sorting like /api/products/?ordering=price


class ProductDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve the details of a single product by its ID.
    Anyone can access this endpoint.
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    # The 'lookup_field' is 'pk' by default, which is what we want.