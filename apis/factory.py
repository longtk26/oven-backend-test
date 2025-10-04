
from apis.repositories import UserRepository
from apis.service import (
    AuthService,
    UserService,
)


class Factory:
    def __init__(self):
        self.__user_repository = None
        self.__auth_service = None
        self.__user_service = None
        
    def create_user_repository(self):
        if not self.__user_repository:
            self.__user_repository = UserRepository()
        return self.__user_repository

    def create_auth_service(self):
        if not self.__auth_service:
            user_repo = self.create_user_repository()
            user_service = self.create_user_service()
           
            self.__auth_service = AuthService(
                    user_repository=user_repo,
                    user_service=user_service
            )
           
        return self.__auth_service
    
    def create_user_service(self):
        if not self.__user_service:
            user_repo = self.create_user_repository()
            # Use lazy injection - pass factory reference instead of auth_service
            self.__user_service = UserService(
                user_repository=user_repo,
            )
        return self.__user_service


# Singleton instance
factory = Factory()
