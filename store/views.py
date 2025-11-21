from django.shortcuts import render

# DRF imports
from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Models
from .models import Product, Category
from django.contrib.auth import get_user_model

User = get_user_model()  # <-- Use custom user model

# Serializers
from .serializers import ProductSerializer, CategorySerializer

# -------------------------------
# Serializer for user registration
# -------------------------------
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# -------------------------------
# Registration view
# -------------------------------
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# -------------------------------
# Cart view (dummy implementation)
# -------------------------------
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"items": [], "total_price": 0})

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        return Response({"message": f"Added product {product_id} x{quantity} to cart"})

# -------------------------------
# Order view (dummy implementation)
# -------------------------------
class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"orders": []})

    def post(self, request):
        return Response({"message": "Order placed successfully"})

# -------------------------------
# Category and Product viewsets
# -------------------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['price', 'name']
    search_fields = ['name', 'description', 'category__name']
