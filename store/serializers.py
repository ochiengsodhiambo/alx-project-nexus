from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, Order, OrderDetail,Seller

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id','product','quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id','buyer','total_price','items']

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(
        required=True,
        help_text="ID of the product to add to cart"
    )
    quantity = serializers.IntegerField(
        required=False,
        default=1,
        help_text="Quantity of the product(s) to add"
    )
        
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
