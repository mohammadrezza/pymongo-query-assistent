from assistant_app.Models.Base import BaseModel

from assistant_app.Models.UserGender import UserGender


class User(BaseModel):
    def __init__(self, id_=-1):
        BaseModel.__init__(self, id_)
        self.full_name: str = ""
        self.username: str = ""
        self.pwd: str = ""
        self.auth: str = ""
        self.gender: UserGender = UserGender.Unknown
        self.img: str = ""
        self.last_login: str = ""

    @staticmethod
    def get_collection_name():
        return "Users"
