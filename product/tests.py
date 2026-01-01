from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Category, Product, Review, Cart, CartItem
from .serializers import ProductSerializer, ProductDetailSerializer

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', is_trending=True)
        self.user = User.objects.create_user(username='testuser', password='password')
        self.product = Product.objects.create(
            name='Smartphone',
            description='A great phone',
            price=999.99,
            category=self.category,
            color='Black'
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Electronics')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Smartphone')

    def test_review_creation(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='Awesome!'
        )
        self.assertEqual(str(review), f"Review for {self.product.name} by {self.user.username}")

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Clothing')
        self.product = Product.objects.create(
            name='T-Shirt',
            description='Cotton t-shirt',
            price=20.00,
            category=self.category
        )
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_get_product_list(self):
        url = reverse('products:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_detail(self):
        url = reverse('products:product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'T-Shirt')

    def test_create_review_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('products:product-review-create', args=[self.product.id])
        data = {'rating': 5, 'comment': 'Nice shirt'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_unauthenticated(self):
        url = reverse('products:product-review-create', args=[self.product.id])
        data = {'rating': 5, 'comment': 'Nice shirt'}
        response = self.client.post(url, data)
        # DRF can return 401 or 403 depending on settings
        self.assertTrue(response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
