from enum import Enum
from flask import Response
from flask_api import status


def dump_class(cls, recursive=False, update_subclass=False):
    """
    :param cls: object in class level, for manual manipulation
    :param recursive: set true if you want to convert a class and subclasses to one dict
    :param update_subclass: set true if you want to update all subclasses in DB
    :return: dictionary containing object data in database level, ready to save
    """
    if not hasattr(cls, "__dict__"):
        return cls

    class_dict = cls.__dict__
    dump_dict = cls.__dict__.copy()
    for key, value in class_dict.items():
        val_type = type(value)

        if val_type in [int, float, str, bool]:
            dump_dict[key] = val_type(value)

        elif type(val_type) == type(Enum):
            dump_dict[key] = value.value

        elif value is None:
            dump_dict[key] = None

        elif val_type == list:
            if recursive:
                tempList = []
                for element in value:
                    tempList.append(dump_class(element, recursive=True))
                dump_dict[key] = tempList
            else:
                dump_dict[key] = val_type(value)

        elif val_type == dict:
            if recursive:
                tempDict = dict()
                for dictKey, dictValue in value.items():
                    tempDict[dictKey] = dump_class(dictValue, recursive=True)
                dump_dict[key] = tempDict
            else:
                dump_dict[key] = val_type(value)

        else:
            if recursive is False:
                if update_subclass:
                    value.UpdateDatabase()  # Making sure it has an ID
                dump_dict[key] = value.ID
            else:
                dump_dict[key] = dump_class(value, recursive=True)

    return dump_dict


def load_class(dict_data, class_type):
    """
    :param dict_data: a dictionary containing target class data
    :param class_type: type of target class name to load data in
    :return: object in class level, filled with right data
    """
    if type(dict_data) != dict:
        return None

    # creating new instance of the target class
    final_class = class_type()
    for key, value in final_class.__dict__.items():
        try:
            value_type = type(value)
            setattr(final_class, key, value_type(dict_data[key]))
        except Exception as e:
            pass
    return final_class


def api_exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(response=e.__str__(), status=status.HTTP_400_BAD_REQUEST)

    wrapper.__name__ = func.__name__
    return wrapper
