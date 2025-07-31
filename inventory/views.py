from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ProductSerializer, SingleProductSerializer
from .models import Product


class ProductAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role not in ["admin", "moderator"]:
            return Response({"errors": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleProductAPIView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        products = Product.objects.filter(pk=pk)
        serializer = SingleProductSerializer(products)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role not in ["admin", "moderator"]:
            return Response({"errors": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist():
            return Response({"error": "product doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SingleProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role not in ["admin", "moderator"]:
            return Response({"errors": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist():
            return Response({"error": "product doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role != "admin":
            return Response({"errors": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        product = Product.objects.get(pk=pk)
        if Product.DoesNotExist():
            return Response({"error": "No product found with this data"}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "product deleted"}, status=status.HTTP_202_ACCEPTED)

