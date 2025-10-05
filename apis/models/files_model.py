from django.db import models
import uuid


class FileModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1024)
    file_size = models.BigIntegerField()
    file_type = models.CharField(max_length=100)
    file_data = models.BinaryField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    # Auto create uuid
    def save(self, *args, **kwargs):
        if not self.id:

            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "files"
        indexes = [
            models.Index(fields=["file_name"]),
            models.Index(fields=["created_at"]),
        ]