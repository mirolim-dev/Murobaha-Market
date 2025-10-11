from rest_framework import serializers
from .models import Category, Product, ProductImage

# --- Nested Serializer for Images ---
class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductImage model.
    """
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


# --- Main Serializers ---
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'is_trending']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model, used for LIST views.
    This provides a more concise overview of the product.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    # For the list view, we'll just show the primary image URL
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'category', 'category_name', 'main_image'
        ]

    def get_main_image(self, obj):
        # 'obj' is the Product instance
        # Get the first image associated with the product, if it exists
        first_image = obj.images.first()
        if first_image:
            return first_image.image
        return None  # Return null if no images are associated


class ProductDetailSerializer(ProductSerializer):
    """
    Serializer for the Product model, used for the DETAIL view.
    It inherits from ProductSerializer and adds more fields, including all images.
    """
    # Nest the ProductImageSerializer to include all images in the detail view
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta(ProductSerializer.Meta):
        # Inherit fields from the parent and add new ones
        fields = ProductSerializer.Meta.fields + [
            'description', 'images', 'color'
        ]