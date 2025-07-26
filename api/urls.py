from django.urls import path
from .views import getUsers, createUsers, login

urlpatterns = [
    path("users/", getUsers, name="get_users"),
    path("users/create/", createUsers, name="create_user"),
    path("users/login/", login, name="login")
]
