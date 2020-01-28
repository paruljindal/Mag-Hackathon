import json
from .messages import Messages
from .constants import Constants


class JsonHandler:
    def __init__(self):
        pass

    @staticmethod
    def get_json():
        path = "app/Content/model.json"
        with open(path, "r") as f:
            json_data = f.read()
        return json_data

    @staticmethod
    def parse_json():
        path = "app/Content/model.json"
        with open(path, "r") as f:
            json_obj = json.load(f)
        return json_obj

    @staticmethod
    def save_json(data_from_user, file_name):
        path = "app/Content/" + file_name
        with open(path, "w") as f:
            f.write(data_from_user)
        f.close()

    @staticmethod
    def get_fallback():
        src = "/app/Content/fallback.json"
        destination = "app/Content/model.json"
        with open(src, "r") as source, open(destination, "w+") as destination:
            destination.write(source.read())
        destination.close()

    @staticmethod
    def parse_user_file(file_name):
        path = "app/Content/" + file_name
        with open(path, "r") as f:
            json_obj = json.load(f)
        return json_obj

    @staticmethod
    def model_validator(filename):
        path = "app/Content/" + filename + ".json"
        with open(path, "r") as f:
            file_data = json.load(f)
        if file_data[Constants.TYPE] not in Constants.ALLOWED_LIST:
            return Messages.VALIDATION_ERROR
        for obj in file_data[Constants.INNER_OBJECT]:
            for obj_name in obj[Constants.NAME_VARIABLE]:
                if obj_name[Constants.NAME] == "" or obj_name[Constants.TYPE] == "":
                    return Messages.VALIDATION_ERROR
            for obj_association in obj[Constants.ASSOCIATIONS]:
                if not ((obj_association[Constants.IDENTIFIER] in Constants.CLASSMAPPING and file_data[
                    Constants.TYPE] == "CLASS") or (
                                obj_association[Constants.IDENTIFIER]
                                in Constants.TABLEMAPPING and file_data[Constants.TYPE] == "TABLE")):
                    return Messages.VALIDATION_ERROR
                for prop in obj_association[Constants.DIRECTION_MAPPING][Constants.CARDINALITY]:
                    if prop[Constants.CARDINALITY]["min"] == "0" or prop[Constants.CARDINALITY]["max"] == "0":
                        return Messages.VALIDATION_ERROR
        return Messages.VALIDATION_SUCCESS
