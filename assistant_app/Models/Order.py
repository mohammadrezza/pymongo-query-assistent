from assistant_app.Models.Base import BaseModel


class Order(BaseModel):
    def __init__(self, id_=-1):
        BaseModel.__init__(self, id_)
        self.transaction_id: str = ""
        self.total_price: int = -1
        self.products: list = []

    @staticmethod
    def get_collection_name():
        return "Orders"
