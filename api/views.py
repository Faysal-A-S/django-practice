
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, MyTokenObtainPairSerializer, UpdateUserSerializer


class UserAPIView(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role not in ["admin", "moderator"]:
            return Response({"errors": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        if User.objects.filter(email=request.data.get("email")):
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleUserAPIView(APIView):
    def patch(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role not in ["admin", "moderator"]:
            return Response({"errors": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist():
            return Response({"error": "user doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateUserSerializer(
            user, data=request.data, partial=True)
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
            user = User.objects.get(pk=pk)
        except User.DoesNotExist():
            return Response({"error": "user doesn't exists"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"errors": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role != "admin":
            return Response({"errors": "No permission"}, status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(pk=pk)
        if User.DoesNotExist():
            return Response({"error": "No user found with this data"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "user deleted"}, status=status.HTTP_202_ACCEPTED)


class UserLogin(APIView):

    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
