from datetime import datetime
from assistant_app.utility import load_class, dump_class
from assistant_app.Models.Query import *


class BaseModel:
    def __init__(self, id_):
        self.id_: int = id_
        self.creation_time = ''

    def load_db(self, id_):
        if type(id_) != int:
            id_ = int(id_)

        # retrieve a dict from db
        query_res: dict = AggregateQuery(self.get_collection_name()).match({"id_": id_}).limit(1).execute()

        # load new object in current class
        if len(query_res) > 0:
            self.__dict__ = load_class(query_res[0], self.__class__).__dict__

    def insert_db(self):
        # convert class data to dict
        class_dict = dump_class(self, update_subclass=True)
        # class_dict.pop("collection_name", None)
        # insert new record in db
        self.creation_time = str(datetime.now())
        class_dict['creation_time'] = self.creation_time
        class_dict['updated'] = self.creation_time
        self.id_, object_id = InsertQuery(self.get_collection_name(), class_dict).execute()
        class_dict.pop("_id", None)
        return object_id, class_dict

    def update_db(self):
        # convert class data to dict
        class_dict = dump_class(self, update_subclass=True)
        class_dict.pop("collection_name", None)
        # we have to update an exiting record
        class_dict['updated'] = str(datetime.now())
        updated_existing = UpdateQuery(self.get_collection_name(), class_dict).add_filter(
            {'id_': self.id_}).execute()
        if updated_existing:
            return class_dict
        else:
            return None

    def delete_db(self):
        RemoveQuery(self.get_collection_name()).add_filter({'id_': self.id_}).execute()
