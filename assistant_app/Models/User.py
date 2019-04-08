class User():
    def __init__(self, id_=-1):
        self.full_name: str = ""
        self.username: str = ""
        self.pwd: str = ""
        self.auth: str = ""
        self.img: str = ""
        self.last_login: str = ""

    @staticmethod
    def get_collection_name():
        return "Users"
