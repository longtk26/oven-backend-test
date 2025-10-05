
from rest_framework import serializers

class PaginateRequestSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, min_value=1, default=1)
    limit = serializers.IntegerField(required=False, min_value=1, max_value=100, default=10)
    search = serializers.CharField(required=False, allow_blank=True, max_length=100)
    search_fields = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    order_by = serializers.CharField(required=False, allow_blank=True, max_length=50)


class PaginateResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
   