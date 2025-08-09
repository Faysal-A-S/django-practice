
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, MyTokenObtainPairSerializer, UpdateUserSerializer
from .permissions import IsAdmin, IsModerator, IsAdminOrModerator
from rest_framework.permissions import IsAuthenticated


class UserAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            return [IsAuthenticated(), IsAdminOrModerator()]
        return super().get_permissions()

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if User.objects.filter(email=request.data.get("email")).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleUserAPIView(APIView):
    def get_permissions(self):
        if self.request.method in ["PATCH", "PUT"]:
            return [IsAuthenticated(), IsAdminOrModerator()]
        elif self.request.method == "DELETE":
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "user doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "user doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "No user found with this data"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "user deleted"}, status=status.HTTP_202_ACCEPTED)


class UserLogin(APIView):
    def post(self, request):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            response = [{
                "access_token": serializer.validated_data["access"],
                "id": serializer.validated_data["id"]
            }]
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
