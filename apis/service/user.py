
from apis.repositories import (
    UserRepository
)
from apis.exceptions import NotFoundException
from apis.exceptions.error_codes import (
    UserErrorCode
)

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def get_user_profile(self, user_id):
        user = self.__user_repository.find_one(id=user_id)

        if not user:
            raise NotFoundException("User not found", code=UserErrorCode.USER_NOT_FOUND.value)

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "abc": "xyz"
        }
   