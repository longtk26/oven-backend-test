
from apis.repositories import ProductsRepository
from apis.repositories.files_repository import FilesRepository, ProductFilesRepository
from apis.service import (
    ProductsService,
)
from apis.service.files_service import FilesService
from libs.file_tree import FileTreeStructure

class Factory:
    def __init__(self):
        self.__products_repository = None
        self.__products_service = None
        self.__files_repository = None
        self.__product_files_repository = None
        self.__files_service = None
        self.__file_tree = None
        
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

    def create_files_repository(self):
        if not self.__files_repository:
            self.__files_repository = FilesRepository()
        return self.__files_repository
    
    def create_product_files_repository(self):
        if not self.__product_files_repository:
            self.__product_files_repository = ProductFilesRepository()
        return self.__product_files_repository
    
    def create_files_service(self):
        if not self.__files_service:
            files_repo = self.create_files_repository()
            product_files_repo = self.create_product_files_repository()
            products_repo = self.create_products_repository()
            file_tree = self.create_file_tree()
            self.__files_service = FilesService(
                files_repository=files_repo,
                product_files_repository=product_files_repo,
                products_repository=products_repo,
                file_tree=file_tree
            )
        return self.__files_service
    
    def create_file_tree(self):
        if not self.__file_tree:
            self.__file_tree = FileTreeStructure() 
        return self.__file_tree

    

factory = Factory()
