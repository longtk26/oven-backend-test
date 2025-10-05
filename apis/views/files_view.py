from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from libs import serializer
from libs.response import make_response
from apis.serializer.files_serializer import (
    UploadFileRequestSerializer,
    UploadFileResponseSerializer,
)
from http import HTTPStatus
from apis.factory import factory
import logging

logger = logging.getLogger(__name__)


class FileUploadView(generics.CreateAPIView):
    """
    File Upload View
    ---
    post: Upload a single file
    Upload a file to the server and optionally associate it with a product.
    Supports folder organization and file type classification.
    """
    parser_classes = [MultiPartParser, FormParser]
    
    @serializer(body=UploadFileRequestSerializer)
    def post(self, body):
        try:
            files_service = factory.create_files_service()

            response = files_service.upload_file(body=body)
            return make_response(
                serializer_class=UploadFileResponseSerializer,
                data=response,
                status_code=HTTPStatus.CREATED,
            )
        except Exception as e:
            logger.error(f"Error in file upload: {str(e)}")
            raise

