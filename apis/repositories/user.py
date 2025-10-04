
from libs import BaseRepository
from apis.models import UserModel

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=UserModel)