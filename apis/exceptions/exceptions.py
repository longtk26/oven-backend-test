from rest_framework.exceptions import APIException
from http import HTTPStatus


class NotFoundException(APIException):
    status_code = HTTPStatus.NOT_FOUND
    default_detail = "Resource not found"
    default_code = "NOT_FOUND"
    code: str

    def __init__(self, detail=None, code=None):
        self.code = code or self.default_code
        super().__init__(detail, code)

class UnauthorizedException(APIException):
    status_code = HTTPStatus.UNAUTHORIZED
    default_detail = "Unauthorized"
    default_code = "UNAUTHORIZED"
    code: str

    def __init__(self, detail=None, code=None):
        self.code = code or self.default_code
        super().__init__(detail, code)


class BadRequestException(APIException):
    status_code = HTTPStatus.BAD_REQUEST
    default_detail = "Bad request"
    default_code = "BAD_REQUEST"
    code: str

    def __init__(self, detail=None, code=None):
        self.code = code or self.default_code
        super().__init__(detail, code)