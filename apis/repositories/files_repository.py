from libs.repositories.base_repository import BaseRepository
from apis.models.files_model import FileModel
from apis.models.product_files_model import ProductFileModel
import os
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class FilesRepository(BaseRepository):
    """Repository for file operations"""
    
    def __init__(self):
        super().__init__(FileModel)
    
    def create_file_record(self, file_data: dict) -> FileModel:
        """Create a new file record in the database"""
        return self.create(file_data)
    
    def save_uploaded_file(self, uploaded_file, folder_path: str = "") -> dict:
        """
        Save uploaded file to local storage and return file info
        
        Args:
            uploaded_file: Django UploadedFile object
            folder_path: Optional folder path within media directory
            
        Returns:
            Dictionary with file information
        """
        # Generate unique filename to prevent conflicts
        file_extension = os.path.splitext(uploaded_file.name)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Construct the full path
        if folder_path:
            full_path = os.path.join(folder_path, unique_filename)
        else:
            full_path = unique_filename
        
        # Save file to storage
        file_path = default_storage.save(full_path, ContentFile(uploaded_file.read()))
        
        # Get file size
        file_size = default_storage.size(file_path)
        
        return {
            'original_name': uploaded_file.name,
            'stored_name': unique_filename,
            'file_path': file_path,
            'file_size': file_size,
            'content_type': uploaded_file.content_type or 'application/octet-stream',
        }
    
    
class ProductFilesRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProductFileModel)

    def create_product_file_association(self, product_id: str, file_id: str, file_type: str = None) -> ProductFileModel:
        """Create association between product and file"""
        return ProductFileModel.objects.create(
            id=uuid.uuid4(),
            product_id=product_id,
            file_id=file_id,
            type=file_type
        )
      