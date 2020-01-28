class RightAssociations:
    def __init__(self, object, cardinality):
        self._object = object
        self._cardinality = cardinality

    def get_object(self):
        return self._object

    def get_cardinality(self):
        return self._cardinality
