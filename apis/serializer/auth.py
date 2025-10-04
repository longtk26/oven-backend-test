
from rest_framework import serializers
from libs import BaseSerializer

class SignUpRequestSerializer(BaseSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)

class SignUpResponseSerializer(BaseSerializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

class LoginRequestSerializer(BaseSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class LoginResponseSerializer(BaseSerializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()