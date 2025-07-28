from django.urls import path
from .views import UserAPIView, UserLogin, ProductAPIView, BrandAPIView, SingleProductView

urlpatterns = [
    path("users/", UserAPIView.as_view(), name="users"),
    # path("users/create/", createUsers, name="create_user"),
    path("users/login/", UserLogin.as_view(), name="login"),
    # path("brands/create/", createBrand, name="create_brand"),
    path("brands/", BrandAPIView.as_view(), name="brands"),
    path("products/", ProductAPIView.as_view(), name="products"),
    path("products/<int:pk>", SingleProductView.as_view(), name="single_product")
    # path("products/create/", createProduct, name="create_product"),
    # path("products/update/<int:pk>/", updateProduct, name="update_product"),
    # path("products/delete/<int:pk>/", deleteProduct, name="delete_product")
]
