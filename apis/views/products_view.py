from rest_framework import generics
from libs import (
    serializer,
)
from libs.response import make_response
from apis.serializer import (
    CreateProductsRequestSerializer,
    CreateProductsResponseSerializer,
    UpdateProductsRequestSerializer,
    UpdateProductsResponseSerializer,
    DeleteProductsResponseSerializer,
    GetProductDetailResponseSerializer,
    ListProductsRequestSerializer,
    ListProductsResponseSerializer,
)
from http import HTTPStatus
from apis.factory import factory


class ListCreateProductsView(generics.ListCreateAPIView):
    """
        Products View
    ---
        post: Create a new product
        Create a new product with the given details.
    """
    @serializer(body=CreateProductsRequestSerializer)
    def post(self, body):
        products_service = factory.create_products_service()
        response = products_service.create_product(product_data=body)
        return make_response(
            serializer_class=CreateProductsResponseSerializer,
            data=response,
            status_code=HTTPStatus.CREATED,
        )

    @serializer(query=ListProductsRequestSerializer)
    def get(self, query):
        products_service = factory.create_products_service()
        response = products_service.list_products(**query)
        return make_response(
            serializer_class=ListProductsResponseSerializer,
            data=response,
            status_code=HTTPStatus.OK,
        )


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        Product Detail View
    ---
        get: Retrieve product details
        Retrieve details of a specific product by its ID.

        put: Update product details
        Update the details of a specific product by its ID.

        delete: Delete a product
        Delete a specific product by its ID.
    """
    @serializer(body=UpdateProductsRequestSerializer)
    def patch(self, product_id, body):
        products_service = factory.create_products_service()
        response = products_service.update_product(product_id=product_id, update_data=body)
        return make_response(
            serializer_class=UpdateProductsResponseSerializer,
            data=response,
            status_code=HTTPStatus.OK,
        )

    @serializer()
    def get(self, product_id):
        products_service = factory.create_products_service()
        response = products_service.get_product(product_id=product_id)
        return make_response(
            serializer_class=GetProductDetailResponseSerializer,
            data=response,
            status_code=HTTPStatus.OK,
        )

    @serializer()
    def delete(self, product_id):
        products_service = factory.create_products_service()
        response = products_service.delete_product(product_id=product_id)
        return make_response(
            serializer_class=DeleteProductsResponseSerializer,
            data=response,
            status_code=HTTPStatus.OK,
        )
    

        



    