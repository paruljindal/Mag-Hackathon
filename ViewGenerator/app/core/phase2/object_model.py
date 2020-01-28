class ObjectModel:
    def __init__(self, alias, name, attributes, associations):
        self._alias = alias
        self._name = name
        self._attributes = attributes
        self._associations = associations

    def get_name(self):
        return self._name

    def get_alias(self):
        return self._alias

    def get_attributes(self):
        return self._attributes

    def get_associations(self):
        return self._associations
