from libs import (
    BaseRepository,
)
from apis.models import (
    ProductModel,
)

class ProductsRepository(BaseRepository):
    def __init__(self):
        super().__init__(ProductModel)