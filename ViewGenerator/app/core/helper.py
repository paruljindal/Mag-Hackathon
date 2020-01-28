from .constants import Constants
import os


class Helper:
    @staticmethod
    def close_file_object(file_object):
        file_object.close()

    @staticmethod
    def open_file_object(class_object, extension):
        if not os.path.exists(Constants.GENERATED):
            os.makedirs(Constants.GENERATED)
        return open(Constants.GENERATED + class_object.get_name() + "." + extension, "w")

    @staticmethod
    def open_file_read_object(file_name, extension):
        return open(Constants.GENERATED + file_name + "." + extension, 'r')

    @staticmethod
    def open_file_object_by_name(_name, extension):
        return open(Constants.GENERATED + _name + "." + extension, "w")
