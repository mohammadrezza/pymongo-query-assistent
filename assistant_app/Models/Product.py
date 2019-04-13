from assistant_app.Models.Base import BaseModel


class Product(BaseModel):
    def __init__(self, id_=-1):
        BaseModel.__init__(self, id_)
        self.name: str = ""
        self.category: str = ""
        self.price: int = -1
        self.specifications: list = []

    @staticmethod
    def get_collection_name():
        return "Products"
