class Attributes:
    def __init__(self, specifier, is_primary, alias, name, type):
        self._specifier = specifier
        self._is_primary = is_primary
        self._alias = alias
        self._name = name
        self._type = type

    def get_specifier(self):
        return self._specifier

    def get_is_primary(self):
        return self._is_primary

    def get_alias(self):
        return self._alias

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type