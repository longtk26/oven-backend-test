
from rest_framework import generics
from libs.decorators import (
    user,
)
from apis.factory import factory
from libs.response import make_response
from apis.serializer.user import UserProfileResponseSerializer

class UserProfileView(generics.GenericAPIView):
    @user()
    def get(self, user):
        user_service = factory.create_user_service()
        user_profile = user_service.get_user_profile(user_id=user['id'])
        return make_response(
            serializer_class=UserProfileResponseSerializer,
            data=user_profile,
        )