from .object_model import ObjectModel
from .attributes import Attributes
from app.core.constants import Constants
from .right_associations import RightAssociations
from .associations import Associations


class ConstructModel:
    def __init__(self):
        pass

    def construct(self, objects):
        objects_model_holder = []
        for object in objects:
            attributes = []
            associations = []
            for attribute in object[Constants.NAME_VARIABLE]:
                name = attribute[Constants.NAME]
                is_primary = attribute[Constants.IS_PRIMARY]
                specifier = attribute[Constants.SPECIFIER]
                alias = attribute[Constants.ALIAS]
                type = attribute[Constants.TYPE]
                attribute_model = Attributes(specifier, is_primary, alias, name, type)
                attributes.append(attribute_model)

            for association in object[Constants.ASSOCIATIONS]:
                right_associations = []
                for right_association in association[Constants.DIRECTION_MAPPING]:
                    object_structure = right_association[Constants.OBJECT]
                    cardinality_structure = right_association[Constants.CARDINALITY]
                    right_association_model = RightAssociations(object_structure, cardinality_structure)
                    right_associations.append(right_association_model)
                identifier = association[Constants.IDENTIFIER]
                association_model = Associations(identifier, right_associations)
                associations.append(association_model)

            alias = object[Constants.ALIAS]
            name = object[Constants.NAME]
            objects_model = ObjectModel(alias, name, attributes, associations)
            objects_model_holder.append(objects_model)
        return objects_model_holder
