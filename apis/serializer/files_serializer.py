from rest_framework import serializers


class UploadFileRequestSerializer(serializers.Serializer):
    """Request serializer for single file upload"""
    file = serializers.FileField(required=True, help_text="File to upload")
    folder_path = serializers.CharField(
        required=True, 
        max_length=255,
        help_text="Folder path for organization"
    )
    product_id = serializers.UUIDField(
        required=False,
        allow_null=True,
        help_text="Optional product ID to associate the file with"
    )
    file_type = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=50,
        help_text="Optional file type classification"
    )



class UploadFileResponseSerializer(serializers.Serializer):
    """Response serializer for single file upload"""
    file_id = serializers.UUIDField()
    file_name = serializers.CharField()
    file_path = serializers.CharField()
    file_size = serializers.IntegerField()
    file_type = serializers.CharField()
    created_at = serializers.CharField()  # ISO format string
    message = serializers.CharField()
    tree_structure = serializers.DictField()
