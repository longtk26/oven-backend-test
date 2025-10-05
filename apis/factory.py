
from apis.repositories import ProductsRepository
from apis.service import (
    ProductsService,
)

class Factory:
    def __init__(self):
        self.__products_repository = None
        self.__products_service = None
        
    def create_products_repository(self):
        if not self.__products_repository:
            self.__products_repository = ProductsRepository()
        return self.__products_repository

    def create_products_service(self):
        if not self.__products_service:
            products_repo = self.create_products_repository()
            self.__products_service = ProductsService(
                products_repository=products_repo
            )
        return self.__products_service

    

factory = Factory()
