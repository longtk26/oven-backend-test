
from rest_framework import serializers

class PaginateRequestSerializer:
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=10)
    search = serializers.CharField(required=False, allow_blank=True, max_length=100)
    ordering = serializers.CharField(required=False, allow_blank=True, max_length=50)


class PaginateResponseSerializer:
    count = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
   