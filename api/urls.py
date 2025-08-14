from django.urls import path
from .views import UserAPIView, UserLogin,  SingleUserAPIView

urlpatterns = [
    path("", UserAPIView.as_view(), name="users"),
    path("<int:pk>", SingleUserAPIView.as_view(), name="user"),
    path("login/", UserLogin.as_view(), name="login"),


]
