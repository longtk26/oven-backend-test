from apis.repositories import (
    UserRepository
)
from apis.serializer import (
    SignUpRequestSerializer,
)
from apis.exceptions import (
    UnauthorizedException,
)
from apis.exceptions.error_codes import (
    AuthErrorCode
)
from .user import UserService

class AuthService:
    def __init__(self, user_repository: UserRepository, user_service: UserService):
        self.__user_repository = user_repository
        self.__user_service = user_service

    def sign_up(self, data: SignUpRequestSerializer):
        data_props = data.props
        # Check if user already exists
        user = self.__user_repository.find_one(email=data_props.email)

        if user:
            # Handle user already exists case
            raise UnauthorizedException("Invalid credentials", AuthErrorCode.INVALID_CREDENTIALS.value)
        
        # Create new user
        new_user = self.user_repository.create(data=data_props.to_dict())

        return {
                "user_id": new_user.id,
                "email": new_user.email,
                "access_token": "dummy_access_token",
                "refresh_token": "dummy_refresh_token"          
            }
    
   