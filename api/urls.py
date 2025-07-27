from django.urls import path
from .views import getUsers, createUsers, login, createBrand, getBrand, getProduct, createProduct, updateProduct, deleteProduct

urlpatterns = [
    path("users/", getUsers, name="get_users"),
    path("users/create/", createUsers, name="create_user"),
    path("users/login/", login, name="login"),
    path("brands/create/", createBrand, name="create_brand"),
    path("brands/", getBrand, name="get_brands"),
    path("products/", getProduct, name="get_products"),
    path("products/create/", createProduct, name="create_product"),
    path("products/update/<int:pk>/", updateProduct, name="update_product"),
    path("products/delete/<int:pk>/", deleteProduct, name="delete_product")
]
