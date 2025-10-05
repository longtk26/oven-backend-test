
from django.urls import path
from apis.views import (
    ListCreateProductsView,
    ProductDetailView,
)

urlpatterns = [
    path("", ListCreateProductsView.as_view(), name="products"),
    path("/<str:product_id>", ProductDetailView.as_view(), name="product_detail"),
]