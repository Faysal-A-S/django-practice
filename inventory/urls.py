from django.urls import path
from .views import ProductAPIView, SingleProductAPIView

urlpatterns = [
    path("", ProductAPIView.as_view(), name="products"),
    path("<int:id>", SingleProductAPIView.as_view(), name="single_product")
]
