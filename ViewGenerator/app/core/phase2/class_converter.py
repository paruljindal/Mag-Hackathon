from .association_model import AssociationModel
from app.core.constants import Constants
from app.core.helper import Helper


class ClassConverter:

    def __init__(self):
        self._output_file_object = {}
        self._main_object_model = {}
        self._required_getter_setter = []

    '''
    Super Private Methods
    '''

    '''
    Static Methods
    '''

    @staticmethod
    def __get_association_model(right_association_mapping):
        associations = []
        for mapping in right_association_mapping:
            class_name = mapping.get_object()[Constants.NAME]
            _min = mapping.get_cardinality()[Constants.MIN]
            _max = mapping.get_cardinality()[Constants.MAX]
            association_model = AssociationModel(class_name, _min, _max)
            associations.append(association_model)
        return associations

    @staticmethod
    def __handle_1_n_mapping(structure, _name):
        structure["member_variables"] += Constants.LIST + "<" + _name + "> m_" + _name.lower() + ";\n"
        structure["parameters"].append(Constants.LIST + "<" + _name + "> " + _name.lower())
        structure["load"] += "\t\t" + Constants.THIS + ".m_" + _name.lower() + " = " \
                             + _name.lower() + ";\n"
        structure["name_parameter"].append("m_" + _name.lower())
        structure["type"].append(Constants.LIST + "<" + _name + "> ")

    @staticmethod
    def __handle_1_1_mapping(structure, _name):
        structure["member_variables"] += _name + " m_" + _name.lower() + ";\n"
        structure["parameters"].append(_name + " " + _name.lower())
        structure["load"] += "\t\t" + Constants.THIS + ".m_" + _name.lower() + " = " \
                             + _name.lower() + ";\n"
        structure["name_parameter"].append("m_" + _name.lower())
        structure["type"].append(_name)

    '''
    Static Methods End
    '''

    def __association_members_add(self, association_models, flag_final, structure):
        for association_model in association_models:
            structure["member_variables"] += "\t"
            _min = association_model.get_association_cardinality_min()
            _max = association_model.get_association_cardinality_max()
            _name = association_model.get_association_name()
            final_string = Constants.FINAL if flag_final == 1 else ""
            structure["member_variables"] += Constants.PRIVATE + " " + final_string + " "
            if _min == '1' and _max == 'N':
                self.__handle_1_n_mapping(structure, _name)
            elif _min == "1" and _max == '1':
                self.__handle_1_1_mapping(structure, _name)
        return structure

    def __fill_constructor(self, load, name):
        self._output_file_object.write(load["member_variables"])
        self._output_file_object.write('\n')
        if name in self._main_object_model:
            self._main_object_model[name]["Parameters"] = load["parameters"]
        self._output_file_object.write(
            "\t" + Constants.PUBLIC + " " + name + "(" + load[
                "parameters"] + ") {\n")
        self._output_file_object.write("\t\t//Super\n" + load["load"])
        self._output_file_object.write("")

    def __association_getter(self, variable, _type):
        self._output_file_object.write("\n")

        self._output_file_object.write(
            "\t" + Constants.PUBLIC + " " + _type + " " + Constants.GET + variable[0].upper()
            + variable[1:] + "() {\n")
        self._output_file_object.write("\t\t" + Constants.RETURN + " " + "this." + variable + ";\n")
        self._output_file_object.write("\t}\n")

    def __generate_getters_setters_association_variable(self, variables, types):
        for index in range(0, len(variables)):
            self.__association_getter(variables[index], types[index])

    def __determine_load(self, class_object):
        structure = {"member_variables": "", "parameters": [], "load": "", "name_parameter": [], "type": []}
        for association_name in class_object.get_associations():
            _type = association_name.get_identifier()
            if _type == Constants.AGGREGATION:
                association_models = self.__get_association_model(association_name.get_right_associations())
                structure = self.__association_members_add(association_models, 0, structure)
            elif _type == Constants.ASSOCIATION:
                association_models = self.__get_association_model(association_name.get_right_associations())
                structure = self.__association_members_add(association_models, 0, structure)
            elif _type == Constants.COMPOSITION:
                association_models = self.__get_association_model(association_name.get_right_associations())
                structure = self.__association_members_add(association_models, 1, structure)
            elif _type == Constants.INHERITANCE:
                # Since One class can have only one right-association in the case of the java inheritance
                if len(association_name.get_right_associations()) > 0:
                    self._main_object_model[class_object.get_name()] \
                        = {"Relationship": association_name.get_right_associations()[0].get_object()[Constants.NAME]}
        structure["parameters"] = ", ".join(structure["parameters"])
        self.__fill_constructor(structure, class_object.get_name())
        self._output_file_object.write("\t}\n")
        self.__generate_getters_setters_association_variable(structure["name_parameter"],
                                                             structure["type"])

    def __generate_variables(self, name, _type, specifier):
        if specifier.lower() == Constants.PRIVATE:
            self._required_getter_setter.append(name)
        self._output_file_object.write("\t" + specifier.lower() + " " + _type + " " + name + ";\n")

    def __generate_getters(self, name, _type):
        self._output_file_object.write("\n")
        self._output_file_object.write(
            "\t" + Constants.PUBLIC + " " + _type + " " + Constants.GET + name[0].upper() + name[
                                                                                            1:] + "() {\n")
        self._output_file_object.write("\t\t" + Constants.RETURN + " " + "this." + name + ";\n")
        self._output_file_object.write("\t}\n")

    def __generate_setters(self, name, _type):
        self._output_file_object.write("\n")
        self._output_file_object.write(
            "\t" + Constants.PUBLIC + " " + Constants.VOID + " " + Constants.SET + name[
                0].upper() + name[
                             1:] + "(" + _type + " " + name + ") {\n")
        self._output_file_object.write("\t\t" + Constants.THIS + "." + name + " = " + name + "; \n")
        self._output_file_object.write("\t}\n")

    '''
    Super Private Methods End
    '''

    '''
    Private Methods
    '''

    def _form_variables(self, class_object):
        for c_object in class_object.get_attributes():
            self.__generate_variables(c_object.get_name(), c_object.get_type(), c_object.get_specifier())

    def _generate_getters_setters(self, class_object):
        for v_object in class_object.get_attributes():
            if v_object.get_name() in self._required_getter_setter:
                self.__generate_getters(v_object.get_name(), v_object.get_type())
                self.__generate_setters(v_object.get_name(), v_object.get_type())

    def _generate_constructors(self, class_object):
        self._output_file_object.write("\n")
        self.__determine_load(class_object)

    def _generate_inheritance_model(self):
        for classes in self._main_object_model:
            if "Relationship" in self._main_object_model[classes]:
                file_object = Helper.open_file_read_object(classes, Constants.EXTENSION)
                file_read = file_object.read()
                file_read = file_read.replace("//Super", "super();")
                file_read = file_read.replace("// extends <CLASS_NAME>",
                                              " extends " + self._main_object_model[classes]["Relationship"])
                file_object_new = Helper.open_file_object_by_name(classes, Constants.EXTENSION)
                file_object_new.write(file_read)
                Helper.close_file_object(file_object)
                Helper.close_file_object(file_object_new)

    '''
    Private Methods End
    '''

    '''
    Public Methods
    '''

    def generate_classes(self, objects):
        for class_object in objects:
            self._required_getter_setter = []
            self._output_file_object = Helper.open_file_object(class_object, Constants.EXTENSION)
            self._output_file_object.write(Constants.PUBLIC + " " + Constants.CLASS_DEF + " " + class_object.get_name()
                                           + "// extends <CLASS_NAME>\n{\n")
            self._form_variables(class_object)
            self._generate_constructors(class_object)
            self._generate_getters_setters(class_object)
            self._output_file_object.write("\t//Functions\n")
            self._output_file_object.write("}\n\n")
            Helper.close_file_object(self._output_file_object)
        self._generate_inheritance_model()
