class Associations:

    def __init__(self, identifier, right_associations):
        self._identifier = identifier
        self._right_associations = right_associations

    def get_identifier(self):
        return self._identifier

    def get_right_associations(self):
        return self._right_associations
