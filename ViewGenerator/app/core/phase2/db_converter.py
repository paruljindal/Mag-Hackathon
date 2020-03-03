from app.core.constants import Constants
from .query_holder import QueryHolder


class DBConverter:
    def __init__(self):
        self._output_file_object = {}
        self._db_objects = {}
        self._main_mapping_tables = ""

    '''
    Super Private Methods
    '''

    def __close_file_object(self):
        self._output_file_object.close()

    def __open_file_object(self, class_object):
        self._output_file_object = open(
            Constants.CONTENT + class_object.get_name() + Constants.DB_EXTENSION, "w")

    def __include_columns(self, attributes, associations, name):
        attributes_array = []
        is_primary = []
        query_holder = {"query": "", "alter_query": ""}
        for attribute in attributes:
            null_allowed = " NOT NULL " if attribute.get_specifier().strip() == "NOT NULL" else "DEFAULT NULL"
            if attribute.get_is_primary():
                is_primary.append("`" + attribute.get_name() + "`")
            attributes_array.append("`" + attribute.get_name() + "` " + attribute.get_type() + " " + null_allowed
                                    + "\n")

        foreign_key = self.__get_association_attributes(associations, name)
        if foreign_key is not None:
            for insert_attribute in foreign_key["insert"]:
                attributes_array.append(insert_attribute)
        attributes_array = "\t,".join(attributes_array)
        primary_keys = ",".join(is_primary)
        primary_keys = "\t," + Constants.PRIMARY + "(" + primary_keys + ")"
        query_holder["query"] += attributes_array
        query_holder["query"] += primary_keys
        if foreign_key is not None:
            if len(foreign_key["foreign_keys"]) > 0:
                keys_append = "\n\t\t\t\t,".join(foreign_key["foreign_keys"])
                query_holder["alter_query"] += "" if keys_append is None else keys_append
        if foreign_key is not None and "mapping" in foreign_key and "name" in foreign_key:
            query_holder["mapping"] = foreign_key["mapping"]
            query_holder["names"] = foreign_key["name"]
        query_holder["query"] += "\n"
        return query_holder

    def __find_info(self, table_name, attribute_name):
        return_type = {"type": "", "specifier": ""}
        primary_key = {"type": "", "specifier": "", "name": ""}
        info_holder = {"return_type": {}, "primary_keys": []}
        for db_object in self._db_objects:
            if db_object.get_name() == table_name:
                for attribute in db_object.get_attributes():
                    if attribute.get_is_primary():
                        return_type["type"] = attribute.get_type()
                        return_type["specifier"] = attribute.get_specifier()
                        primary_key["name"] = attribute.get_name()
                        primary_key["type"] = attribute.get_type()
                        primary_key["specifier"] = attribute.get_specifier()
                        info_holder["return_type"] = return_type
                        info_holder["primary_keys"].append(primary_key)
                    elif attribute.get_name() == attribute_name:
                        return_type["type"] = attribute.get_type()
                        return_type["specifier"] = attribute.get_specifier()
                        info_holder["return_type"] = return_type
        return info_holder

    def __formed_foreign_key(self, right_associations):
        foreign_keys = {"insert": [], "foreign_keys": []}
        for right_association in right_associations:
            object_structure = right_association.get_object()
            foreign_keys["foreign_keys"].append(Constants.ADD + " " +
                                                Constants.FOREIGN_KEY + "(`" + object_structure[
                                                    Constants.LOCAL_ATTRIBUTE] + "`) " + Constants.REFERENCES + " " +
                                                object_structure[
                                                    Constants.NAME] + "(`" + object_structure[
                                                    Constants.ATTRIBUTE] + "`)")
            if object_structure[Constants.IS_INSERT_REQUIRED]:
                return_type = self.__find_info(object_structure[Constants.NAME], object_structure[Constants.ATTRIBUTE])[
                    "return_type"]
                null_allowed = " NOT NULL " if return_type["specifier"].strip() == "NOT NULL" else "DEFAULT NULL"
                foreign_keys["insert"].append(
                    "`" + object_structure[Constants.LOCAL_ATTRIBUTE] + "` " + return_type["type"] + " " + null_allowed
                    + "\n")
        return foreign_keys

    '''
    Special Case of Many to Many Mapping
    '''
    
    def __special_case_mtm_mapping(self, right_associations, name):
        foreign_keys = {"insert": [], "foreign_keys": [], "mapping": {"create_mapping": [], "foreign_keys": []},
                        "name": []}

        for right_association in right_associations:
            object_structure = right_association.get_object()
            foreign_keys["name"].append(object_structure[Constants.NAME])
            info_holder = self.__find_info(object_structure[Constants.NAME], object_structure[Constants.ATTRIBUTE])
            primary_keys = info_holder["primary_keys"]
            create_table_mapping = []
            foreign_keys_mapping = []
            if object_structure[Constants.IS_INSERT_REQUIRED]:
                return_type = self.__find_info(object_structure[Constants.NAME], object_structure[Constants.ATTRIBUTE])[
                    "return_type"]
                null_allowed = " NOT NULL " if return_type["specifier"].strip() == "NOT NULL" else "DEFAULT NULL"
                foreign_keys["insert"].append(
                    "`" + object_structure[Constants.LOCAL_ATTRIBUTE] + "` " + return_type["type"] + " " + null_allowed
                    + "\n")
            local_info = self.__find_info(name, object_structure[Constants.LOCAL_ATTRIBUTE])
            null_allowed = " NOT NULL " if local_info["return_type"][
                                               "specifier"].strip() == "NOT NULL" else "DEFAULT NULL"
            create_table_mapping.append("`" + name + "_" + object_structure[Constants.LOCAL_ATTRIBUTE] + "` "
                                        + local_info["return_type"]["type"] + " " + null_allowed + "\n")
            foreign_keys_mapping.append(Constants.ADD + " " + Constants.FOREIGN_KEY
                                        + "(`" + name + "_" + object_structure[Constants.LOCAL_ATTRIBUTE] + "`) "
                                        + Constants.REFERENCES + " " + name
                                        + "(`" + object_structure[Constants.LOCAL_ATTRIBUTE] + "`)")
            for primary_key in primary_keys:
                null_allowed = " NOT NULL " if primary_key[
                                                   Constants.SPECIFIER].strip() == "NOT NULL" else "DEFAULT NULL"
                create_table_mapping.append("`" + primary_key[Constants.NAME] + "` " + primary_key[Constants.TYPE]
                                            + " " + null_allowed + "\n")
                foreign_keys_mapping.append(Constants.ADD + " " + Constants.FOREIGN_KEY
                                            + "(`" + object_structure[Constants.LOCAL_ATTRIBUTE] + "`) "
                                            + Constants.REFERENCES + " " + object_structure[Constants.NAME]
                                            + "(`" + primary_key[Constants.NAME] + "`)")

            foreign_keys["mapping"]["create_mapping"].append(create_table_mapping)
            foreign_keys["mapping"]["foreign_keys"].append(foreign_keys_mapping)
        return foreign_keys

    def __get_association_attributes(self, associations, name):
        for association in associations:
            identifier = association.get_identifier()
            if identifier == Constants.MANY_TO_MANY:
                # special_case
                return self.__special_case_mtm_mapping(association.get_right_associations(), name)
            elif identifier == Constants.ONE_TO_MANY:
                return self.__formed_foreign_key(association.get_right_associations())
            elif identifier == Constants.ONE_TO_ONE:
                return self.__formed_foreign_key(association.get_right_associations())

    def __form_mm_mapping(self, query_mapper, mm_mappings, names, accessed_table_name):
        query_mapper["alter_query"] += ""
        for mm_mapping_index in range(0, len(mm_mappings["create_mapping"])):
            local_create_query = Constants.CREATE + " " + Constants.TABLE + " `" + accessed_table_name + "_" + names[
                mm_mapping_index] + "` (\n\t\t"
            local_create_query += "\t\t,".join(mm_mappings["create_mapping"][mm_mapping_index]) + "\n)"
            self._main_mapping_tables += local_create_query + "\n\n"
        for mm_mapping_index in range(0, len(mm_mappings["foreign_keys"])):
            local_alter_mapping = Constants.ALTER + " " + Constants.TABLE + " `" + accessed_table_name + "_" + names[
                mm_mapping_index] + "` \n\t\t"
            local_alter_mapping += ",\n\t\t".join(mm_mappings["foreign_keys"][mm_mapping_index]) + "\n"
            query_mapper["alter_query"] += local_alter_mapping + "\n\n"

    '''
    Private Methods
    '''

    def _generate_create_table_queries(self, db_object, query_holder):
        query_holder["query"] += Constants.CREATE + " " + Constants.TABLE + " `" + db_object.get_name() + "` (\n"
        temp_holder = self.__include_columns(db_object.get_attributes(),
                                             db_object.get_associations(), db_object.get_name())
        query_holder["query"] += temp_holder["query"]
        query_holder["query"] += ")\n"

        if temp_holder["alter_query"].strip() != "":
            query_holder["alter_query"] += Constants.ALTER + " " + Constants.TABLE + " `" + db_object.get_name() + "` "
            query_holder["alter_query"] += temp_holder["alter_query"]

        if 'mapping' in temp_holder.keys():
            self.__form_mm_mapping(query_holder, temp_holder["mapping"], temp_holder["names"], db_object.get_name())

    def _format_query_holder(self, query_holders):
        if len(query_holders) > 0:
            query_holder = query_holders[len(query_holders) - 1]
            create_query = query_holder.get_query()
            alter_mapping = query_holder.get_alter_commands()
            query_holders.remove(query_holder)
            create_query += self._main_mapping_tables
            query_holder = QueryHolder(create_query, alter_mapping)
            query_holders.append(query_holder)
        return query_holders

    '''
    Public Methods
    '''

    def db_converter(self, objects):
        self._db_objects = objects
        query_holders = []
        for db_object in objects:
            query_mapper = {"query": "", "alter_query": "", "mapping": []}
            self._generate_create_table_queries(db_object, query_mapper)
            query_holder = QueryHolder(query_mapper["query"], query_mapper["alter_query"])
            query_holders.append(query_holder)
        return self._format_query_holder(query_holders)
