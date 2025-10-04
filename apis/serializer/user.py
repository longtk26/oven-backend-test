
from rest_framework import serializers
from libs import (
    PaginateRequestSerializer,
    PaginateResponseSerializer,
)

class UserProfileResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()

class GetListUsersRequestSerializer(PaginateRequestSerializer):
    pass

class GetListUsersResponseSerializer(PaginateResponseSerializer):
    results = UserProfileResponseSerializer(many=True)