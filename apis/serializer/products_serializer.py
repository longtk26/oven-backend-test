from rest_framework import serializers
from libs import (
    PaginateRequestSerializer,
    PaginateResponseSerializer,
)


# Mutation Serializers
class CreateProductsRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)
    description = serializers.CharField(allow_blank=True, trim_whitespace=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CreateProductsResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    message = serializers.CharField(max_length=255)


class UpdateProductsRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=True, trim_whitespace=True, required=False)
    description = serializers.CharField(allow_blank=True, trim_whitespace=True, required=False)
    price = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2, required=False)

    def validate(self, attrs):
        # Ensure at least one field is provided for update
        if not attrs:
            raise serializers.ValidationError("At least one field must be provided for update.")
        return super().validate(attrs)

class UpdateProductsResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    message = serializers.CharField(max_length=255)


class DeleteProductsResponseSerializer(serializers.Serializer):
    deleted_count = serializers.IntegerField()
    message = serializers.CharField(max_length=255)


# Query Serializers

class GetProductDetailResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class ListProductsRequestSerializer(PaginateRequestSerializer):
    pass

class ListProductsResponseSerializer(PaginateResponseSerializer):
    products = GetProductDetailResponseSerializer(many=True)