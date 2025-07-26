from rest_framework import serializers
from .models import User, Product, Brand
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', "password"]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', "create_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'description',
                  'price', 'created_at', 'updated_at']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = 'email'
