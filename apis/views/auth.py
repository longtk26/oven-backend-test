from rest_framework import generics
from rest_framework.response import Response
from apis.serializer.auth import (
    SignUpRequestSerializer,
    SignUpResponseSerializer,
    LoginRequestSerializer,
)
from apis.factory import factory
from libs.decorators import (
    serializer,
    public
)

from libs.response import make_response
from http import HTTPStatus

class SignUpView(generics.GenericAPIView):

    @public
    @serializer(body=SignUpRequestSerializer)
    def post(self, body):
        auth_service = factory.create_auth_service()
        response = auth_service.sign_up(data=body)
        return make_response(SignUpResponseSerializer, response, status_code=HTTPStatus.CREATED)


class LoginView(generics.GenericAPIView):
    @public
    @serializer(body=LoginRequestSerializer)
    def post(self, body):
        return NotImplementedError()

