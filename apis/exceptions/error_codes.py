from enum  import Enum

class AuthErrorCode(Enum):
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"

class UserErrorCode(Enum):
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"