from rest_framework import serializers
from .models import Brand, Product, Category


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all())

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = "__all__"


class SingleProductSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), required=False)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields in self.fields.values():
            fields.required = False


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
