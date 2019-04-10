from collections import *
from pymongo import command_cursor
from assistant_app import app
from assistant_app import mongo


class BaseQuery:
    collections = dict()
    with app.app_context():
        for coll in mongo.db.collection_names():
            collections[coll] = getattr(mongo.db, str(coll))

    def __init__(self, coll_name):
        self.result = None
        self.collection = self.collections[coll_name]

    def return_result(self):
        if type(self.result) == dict:
            check = self.result.get("result", "")
            if check == "":
                return list(self.result)
            else:
                return self.result["result"]
        elif type(self.result) == command_cursor.CommandCursor:
            return list(self.result)
        elif type(self.result) == list:
            return self.result
        else:
            return list()


class AggregateQuery(BaseQuery):
    def __init__(self, coll_name):
        super(AggregateQuery, self).__init__(coll_name)
        self.query = []

    def execute(self):
        self.result = list(self.collection.aggregate(self.query))
        return self.return_result()
