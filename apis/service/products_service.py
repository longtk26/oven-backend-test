from apis.repositories import ProductsRepository
from apis.exceptions import (
    NotFoundException,
)
from apis.exceptions.error_codes import (
    ProductErrorCode,
)
import logging

logger = logging.getLogger(__name__)

class ProductsService:

    def __init__(self, products_repository: ProductsRepository):
        self.products_repository = products_repository


    def create_product(self, product_data):
        new_product = self.products_repository.create(product_data)
        
        return {
            "id": new_product.id,
            "message": "Product created successfully",
        }
    
    def update_product(self, product_id, update_data):
        existing_product = self.products_repository.find_one(id=product_id, deleted_at=None)
        if not existing_product:
            raise NotFoundException(
                detail="Product not found",
                code=ProductErrorCode.PRODUCT_NOT_FOUND.value,
            )

        update_code = self.products_repository.update(
            filters={"id": product_id},
            data=update_data
        )

        return {
            "id": update_code,
            "message": "Product updated successfully",
        }

    def delete_product(self, product_id):
        existing_product = self.products_repository.find_one(id=product_id, deleted_at=None)
        
        if not existing_product:
            raise NotFoundException(
                detail="Product not found",
                code=ProductErrorCode.PRODUCT_NOT_FOUND.value,
            )

        count, _ = self.products_repository.delete(id=product_id)

        return {
            "deleted_count": count,
            "message": "Product deleted successfully",
        }
    
    def get_product(self, product_id):
        product = self.products_repository.find_one(id=product_id)

        if not product:
            raise NotFoundException(
                detail="Product not found",
                code=ProductErrorCode.PRODUCT_NOT_FOUND,
            )

        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
        }
    

    def list_products(self, **query_params):
        data, count, total_pages = self.products_repository.paginate(**query_params)

        return {
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                }
                for product in data
            ],
            "count": count,
            "total_pages": total_pages,
            "current_page": query_params.get("page", 1),
        }
