from django.shortcuts import render

# DRF imports
from rest_framework import viewsets, filters, generics,serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Seller
from .serializers import SellerSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import AddToCartSerializer
from store.models import Product
from rest_framework.exceptions import NotFound
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
# Cart view 
# -------------------------------
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="View the current cart items",
        responses={200: openapi.Response("Cart retrieved successfully")}
    )
    def get(self, request):
        return Response({"items": [], "total_price": 0})

    @swagger_auto_schema(
        request_body=AddToCartSerializer,
        operation_description="Add an item to the cart",
        responses={
            200: openapi.Response("Product added to cart"),
            400: "Invalid input"
        }
    )
    def post(self, request):
        
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        # Validate
        if not product_id:
            return Response(
                {"error": "product_id is required"},
                status=400
            )

        # Fetch product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

        # Normally you'd save to Cart model. For now we simulate the cart return
        total_value = float(product.price) * quantity

        return Response({
            "message": "Product added to cart",
            "cart": {
                "product_id": product.id,
                "product_name": product.name,
                "price_each": str(product.price),
                "quantity": quantity,
                "total_value": total_value
            }
        })

# -------------------------------
# Order view 
# -------------------------------

class PlaceOrderSerializer(serializers.Serializer):
    payment_method = serializers.CharField()
    shipping_address = serializers.CharField()

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="show all orders for the authenticated user",
        responses={200: openapi.Response("Orders retrieved successfully")}
    )
    def get(self, request):
        return Response({"orders": []})

    @swagger_auto_schema(
        request_body=PlaceOrderSerializer,
        operation_description="Place a new order",
        responses={
            200: openapi.Response("Order placed successfully"),
            400: "Invalid request"
        }
    )
    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_method = serializer.validated_data['payment_method']
        shipping_address = serializer.validated_data['shipping_address']

        return Response({
            "message": "Order placed successfully",
            "payment_method": payment_method,
            "shipping_address": shipping_address
        })

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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search products by name, description or category",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order by price or name",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# -------------------------------
# Seller viewset
# -------------------------------
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer