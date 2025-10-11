from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image_url = models.URLField(max_length=500, null=True)
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    # For multiple product images, a separate ProductImage model can be created

    def __str__(self):
        return self.name
    
    def get_product_images(self):
        ''' Returns a queryset of all images related to this product. '''
        return self.images.values('image')  

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
