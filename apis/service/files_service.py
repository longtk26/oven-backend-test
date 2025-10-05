import os
import logging
from typing import  Dict, Any
from django.core.files.uploadedfile import UploadedFile
from apis.repositories.files_repository import FilesRepository, ProductFilesRepository
from apis.repositories.products_repository import ProductsRepository
from libs.file_tree.file_tree import FileTreeStructure
from apis.exceptions import NotFoundException, BadRequestException
from apis.exceptions.error_codes import ProductErrorCode
from django.db import transaction

logger = logging.getLogger(__name__)


class FilesService:
    """Service for file upload and management operations"""
    
    def __init__(
        self, 
        files_repository: FilesRepository,
        product_files_repository: ProductFilesRepository,
        products_repository: ProductsRepository,
        file_tree: FileTreeStructure 
    ):
        self.files_repository = files_repository
        self.product_files_repository = product_files_repository
        self.products_repository = products_repository
        self.file_tree = file_tree
    
    @transaction.atomic
    def upload_file(
        self, 
        body: dict = None
    ) -> Dict[str, Any]:
        """
        Upload a file and optionally associate it with a product
        
        Args:
            uploaded_file: The uploaded file
            folder_path: Optional folder path for organization
            product_id: Optional product ID to associate the file with
            file_type: Optional file type classification
            
        Returns:
            Dictionary with upload result
        """
        try:
            uploaded_file: UploadedFile = body.get('file') 
            product_id: str = str(body.get('product_id')) if body.get('product_id') else None  
            folder_path: str = str(body.get('folder_path', ''))
            file_type: str = str(body.get('file_type', ''))

            # Validate file
            if not uploaded_file:
                raise BadRequestException("No file provided")
            
            # Validate file size (limit to 50MB)
            max_size = 50 * 1024 * 1024  # 50MB
            if uploaded_file.size > max_size:
                raise BadRequestException(f"File size exceeds maximum limit of {max_size} bytes")
            
            # Validate product exists if product_id is provided
            if product_id:
                product = self.products_repository.find_one(id=product_id, deleted_at=None)
                if not product:
                    raise NotFoundException(
                        detail="Product not found",
                        code=ProductErrorCode.PRODUCT_NOT_FOUND.value,
                    )
            
            # Save file to storage
            file_info = self.files_repository.save_uploaded_file(uploaded_file, folder_path)
            
            # Create file record in database
            file_data = {
                'file_name': file_info['original_name'],
                'file_path': file_info['file_path'],
                'file_size': file_info['file_size'],
                'file_type': file_info['content_type'],
                'file_data': b'',  
            }
            
            file_record = self.files_repository.create_file_record(file_data)
            
            # Add to file tree structure
            tree_path = os.path.join(folder_path, file_info['original_name']) if folder_path else file_info['original_name']
            self.file_tree.add_file(
                file_path=tree_path,
                file_size=file_info['file_size'],
                created_at=file_record.created_at,
                modified_at=file_record.updated_at
            )
            
            # Associate with product if provided
            if product_id:
                self.product_files_repository.create_product_file_association(
                    product_id=product_id,
                    file_id=str(file_record.id),
                    file_type=file_type
                )
            
            return {
                "file_id": str(file_record.id),
                "file_name": file_record.file_name,
                "file_path": file_record.file_path,
                "file_size": file_record.file_size,
                "file_type": file_record.file_type,
                "created_at": file_record.created_at.isoformat(),
                "tree_structure": self.file_tree.to_tree_dict(),
                "message": "File uploaded successfully"
            }
            
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise