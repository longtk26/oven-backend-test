import unittest
from unittest.mock import Mock, patch
from decimal import Decimal
import uuid
from django.test import TestCase

from apis.service.products_service import ProductsService
from apis.repositories.products_repository import ProductsRepository
from apis.exceptions.exceptions import NotFoundException
from apis.exceptions.error_codes import ProductErrorCode
from apis.models.products_model import ProductModel


class TestProductsService(TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_repository = Mock(spec=ProductsRepository)
        self.products_service = ProductsService(self.mock_repository)
        
        # Sample product data for testing
        self.sample_product_data = {
            "name": "Test Product",
            "description": "This is a test product",
            "price": Decimal("19.99")
        }
        
        # Sample product model instance
        self.sample_product_id = uuid.uuid4()
        self.sample_product = Mock(spec=ProductModel)
        self.sample_product.id = self.sample_product_id
        self.sample_product.name = "Test Product"
        self.sample_product.description = "This is a test product"
        self.sample_product.price = Decimal("19.99")

    def test_create_product_success(self):
        """Test successful product creation."""
        # Arrange
        self.mock_repository.create.return_value = self.sample_product
        
        # Act
        result = self.products_service.create_product(self.sample_product_data)
        
        # Assert
        self.mock_repository.create.assert_called_once_with(self.sample_product_data)
        self.assertEqual(result["id"], self.sample_product_id)
        self.assertEqual(result["message"], "Product created successfully")

    def test_update_product_success(self):
        """Test successful product update."""
        # Arrange
        product_id = self.sample_product_id
        update_data = {"name": "Updated Product Name"}
        expected_update_count = 1
        
        self.mock_repository.find_one.return_value = self.sample_product
        self.mock_repository.update.return_value = expected_update_count
        
        # Act
        result = self.products_service.update_product(product_id, update_data)
        
        # Assert
        self.mock_repository.find_one.assert_called_once_with(id=product_id, deleted_at=None)
        self.mock_repository.update.assert_called_once_with(
            filters={"id": product_id},
            data=update_data
        )
        self.assertEqual(result["id"], expected_update_count)
        self.assertEqual(result["message"], "Product updated successfully")

    def test_update_product_not_found(self):
        """Test updating a non-existent product raises NotFoundException."""
        # Arrange
        product_id = uuid.uuid4()
        update_data = {"name": "Updated Product Name"}
        
        self.mock_repository.find_one.return_value = None
        
        # Act & Assert
        with self.assertRaises(NotFoundException) as context:
            self.products_service.update_product(product_id, update_data)
        
        self.assertEqual(str(context.exception.detail), "Product not found")
        self.assertEqual(context.exception.code, ProductErrorCode.PRODUCT_NOT_FOUND.value)
        self.mock_repository.find_one.assert_called_once_with(id=product_id, deleted_at=None)
        self.mock_repository.update.assert_not_called()

    def test_delete_product_success(self):
        """Test successful product deletion."""
        # Arrange
        product_id = self.sample_product_id
        expected_deleted_count = 1
        
        self.mock_repository.find_one.return_value = self.sample_product
        self.mock_repository.delete.return_value = (expected_deleted_count, {})
        
        # Act
        result = self.products_service.delete_product(product_id)
        
        # Assert
        self.mock_repository.find_one.assert_called_once_with(id=product_id, deleted_at=None)
        self.mock_repository.delete.assert_called_once_with(id=product_id)
        self.assertEqual(result["deleted_count"], expected_deleted_count)
        self.assertEqual(result["message"], "Product deleted successfully")

    def test_delete_product_not_found(self):
        """Test deleting a non-existent product raises NotFoundException."""
        # Arrange
        product_id = uuid.uuid4()
        
        self.mock_repository.find_one.return_value = None
        
        # Act & Assert
        with self.assertRaises(NotFoundException) as context:
            self.products_service.delete_product(product_id)
        
        self.assertEqual(str(context.exception.detail), "Product not found")
        self.assertEqual(context.exception.code, ProductErrorCode.PRODUCT_NOT_FOUND.value)
        self.mock_repository.find_one.assert_called_once_with(id=product_id, deleted_at=None)
        self.mock_repository.delete.assert_not_called()

    def test_get_product_success(self):
        """Test successful product retrieval."""
        # Arrange
        product_id = self.sample_product_id
        
        self.mock_repository.find_one.return_value = self.sample_product
        
        # Act
        result = self.products_service.get_product(product_id)
        
        # Assert
        self.mock_repository.find_one.assert_called_once_with(id=product_id)
        self.assertEqual(result["id"], self.sample_product_id)
        self.assertEqual(result["name"], "Test Product")
        self.assertEqual(result["description"], "This is a test product")
        self.assertEqual(result["price"], Decimal("19.99"))

    def test_get_product_not_found(self):
        """Test getting a non-existent product raises NotFoundException."""
        # Arrange
        product_id = uuid.uuid4()
        
        self.mock_repository.find_one.return_value = None
        
        # Act & Assert
        with self.assertRaises(NotFoundException) as context:
            self.products_service.get_product(product_id)
        
        self.assertEqual(str(context.exception.detail), "Product not found")
        self.assertEqual(context.exception.code, ProductErrorCode.PRODUCT_NOT_FOUND)
        self.mock_repository.find_one.assert_called_once_with(id=product_id)

    def test_list_products_success(self):
        """Test successful product listing with pagination."""
        # Arrange
        product1 = Mock(spec=ProductModel)
        product1.id = uuid.uuid4()
        product1.name = "Product 1"
        product1.description = "Description 1"
        product1.price = Decimal("10.00")
        
        product2 = Mock(spec=ProductModel)
        product2.id = uuid.uuid4()
        product2.name = "Product 2"
        product2.description = "Description 2"
        product2.price = Decimal("20.00")
        
        mock_products = [product1, product2]
        total_count = 2
        total_pages = 1
        
        self.mock_repository.paginate.return_value = (mock_products, total_count, total_pages)
        
        query_params = {"page": 1, "limit": 10}
        
        # Act
        result = self.products_service.list_products(**query_params)
        
        # Assert
        self.mock_repository.paginate.assert_called_once_with(**query_params)
        
        self.assertEqual(len(result["products"]), 2)
        self.assertEqual(result["count"], total_count)
        self.assertEqual(result["total_pages"], total_pages)
        self.assertEqual(result["current_page"], 1)
        
        # Check first product
        self.assertEqual(result["products"][0]["id"], product1.id)
        self.assertEqual(result["products"][0]["name"], "Product 1")
        self.assertEqual(result["products"][0]["description"], "Description 1")
        self.assertEqual(result["products"][0]["price"], Decimal("10.00"))
        
        # Check second product
        self.assertEqual(result["products"][1]["id"], product2.id)
        self.assertEqual(result["products"][1]["name"], "Product 2")
        self.assertEqual(result["products"][1]["description"], "Description 2")
        self.assertEqual(result["products"][1]["price"], Decimal("20.00"))

    def test_list_products_empty_result(self):
        """Test listing products when no products exist."""
        # Arrange
        mock_products = []
        total_count = 0
        total_pages = 0
        
        self.mock_repository.paginate.return_value = (mock_products, total_count, total_pages)
        
        query_params = {"page": 1, "limit": 10}
        
        # Act
        result = self.products_service.list_products(**query_params)
        
        # Assert
        self.mock_repository.paginate.assert_called_once_with(**query_params)
        
        self.assertEqual(len(result["products"]), 0)
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["total_pages"], 0)
        self.assertEqual(result["current_page"], 1)

    def test_list_products_with_custom_page(self):
        """Test listing products with custom page parameter."""
        # Arrange
        mock_products = []
        total_count = 0
        total_pages = 0
        
        self.mock_repository.paginate.return_value = (mock_products, total_count, total_pages)
        
        query_params = {"page": 3, "limit": 5}
        
        # Act
        result = self.products_service.list_products(**query_params)
        
        # Assert
        self.mock_repository.paginate.assert_called_once_with(**query_params)
        self.assertEqual(result["current_page"], 3)

    def test_list_products_default_page(self):
        """Test listing products with default page when not specified."""
        # Arrange
        mock_products = []
        total_count = 0
        total_pages = 0
        
        self.mock_repository.paginate.return_value = (mock_products, total_count, total_pages)
        
        query_params = {"limit": 10}  # No page specified
        
        # Act
        result = self.products_service.list_products(**query_params)
        
        # Assert
        self.mock_repository.paginate.assert_called_once_with(**query_params)
        self.assertEqual(result["current_page"], 1)  # Default page should be 1

    def test_list_products_with_search_and_filters(self):
        """Test listing products with search parameters and filters."""
        # Arrange
        mock_products = [self.sample_product]
        total_count = 1
        total_pages = 1
        
        self.mock_repository.paginate.return_value = (mock_products, total_count, total_pages)
        
        query_params = {
            "page": 1,
            "limit": 10,
            "search": "test",
            "search_fields": ["name", "description"],
            "price__gte": 10.00
        }
        
        # Act
        result = self.products_service.list_products(**query_params)
        
        # Assert
        self.mock_repository.paginate.assert_called_once_with(**query_params)
        self.assertEqual(len(result["products"]), 1)
        self.assertEqual(result["products"][0]["name"], "Test Product")

    @patch('apis.service.products_service.logger')
    def test_service_initialization(self, mock_logger):
        """Test that ProductsService initializes correctly with repository."""
        # Arrange
        repository = Mock(spec=ProductsRepository)
        
        # Act
        service = ProductsService(repository)
        
        # Assert
        self.assertEqual(service.products_repository, repository)

    def test_create_product_with_repository_exception(self):
        """Test create_product handles repository exceptions."""
        # Arrange
        self.mock_repository.create.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.products_service.create_product(self.sample_product_data)
        
        self.assertEqual(str(context.exception), "Database error")
        self.mock_repository.create.assert_called_once_with(self.sample_product_data)

    def test_update_product_with_repository_exception(self):
        """Test update_product handles repository exceptions."""
        # Arrange
        product_id = self.sample_product_id
        update_data = {"name": "Updated Product Name"}
        
        self.mock_repository.find_one.return_value = self.sample_product
        self.mock_repository.update.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.products_service.update_product(product_id, update_data)
        
        self.assertEqual(str(context.exception), "Database error")

    def test_delete_product_with_repository_exception(self):
        """Test delete_product handles repository exceptions."""
        # Arrange
        product_id = self.sample_product_id
        
        self.mock_repository.find_one.return_value = self.sample_product
        self.mock_repository.delete.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.products_service.delete_product(product_id)
        
        self.assertEqual(str(context.exception), "Database error")

    def test_get_product_with_repository_exception(self):
        """Test get_product handles repository exceptions."""
        # Arrange
        product_id = self.sample_product_id
        
        self.mock_repository.find_one.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.products_service.get_product(product_id)
        
        self.assertEqual(str(context.exception), "Database error")

    def test_list_products_with_repository_exception(self):
        """Test list_products handles repository exceptions."""
        # Arrange
        self.mock_repository.paginate.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.products_service.list_products(page=1, limit=10)
        
        self.assertEqual(str(context.exception), "Database error")


if __name__ == '__main__':
    unittest.main()