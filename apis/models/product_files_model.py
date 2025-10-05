from django.db import models


class  ProductFileModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    product = models.ForeignKey(
        "ProductModel", on_delete=models.CASCADE, related_name="files"
    )
    file = models.ForeignKey(
        "FileModel", on_delete=models.CASCADE, related_name="products"
    )
    type = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "product_files"
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["file"]),
        ]