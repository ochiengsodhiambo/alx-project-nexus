from rest_framework import serializers
from .models import User, Buyer, Seller
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password','is_buyer','is_seller']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            is_buyer=validated_data.get('is_buyer', False),
            is_seller=validated_data.get('is_seller', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
