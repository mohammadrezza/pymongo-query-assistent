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

class InsertQuery(BaseQuery):
    def __init__(self, coll_name: str, insert_dict: dict):
        super(InsertQuery, self).__init__(coll_name)
        self.insert_dict = insert_dict

    def execute(self):
        latest_object = list(self.collection.find({}).sort([("id_", -1)]))
        if len(latest_object) > 0:
            # calculating ID , by the length of that collection
            self.insert_dict["id_"] = latest_object[0]["id_"] + 1
        else:
            self.insert_dict["id_"] = 1
        self.result = self.collection.insert(self.insert_dict)
        return self.insert_dict["id_"], str(self.result)


class DistinctQuery(BaseQuery):
    def __init__(self, coll_name: str, filed: str):
        super(DistinctQuery, self).__init__(coll_name)
        self.filed = filed

    def execute(self):
        return list(self.collection.distinct(self.filed))


class UpdateQuery(BaseQuery):
    def __init__(self, coll_name: str, update_dict: dict):
        super(UpdateQuery, self).__init__(coll_name)
        self.update_dict = update_dict
        self.filter = dict()

    def execute(self):
        self.result = self.collection.update(self.filter, self.update_dict)
        return self.result["updatedExisting"]

    def add_filter(self, filter: dict):
        for key, val in filter.items():
            self.filter[key] = val
        return self


class RemoveQuery(BaseQuery):
    def __init__(self, coll_name: str):
        super(RemoveQuery, self).__init__(coll_name)
        self.filter = dict()

    def execute(self):
        self.result = self.collection.remove(self.filter)

    def add_filter(self, filter: dict):
        for key, val in filter.items():
            self.filter[key] = val
        return self
