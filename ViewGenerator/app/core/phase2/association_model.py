class AssociationModel:
    def __init__(self, name, min, max):
        self._association_name = name
        self._association_cardinality_min = min
        self._association_cardinality_max = max

    def get_association_name(self):
        return self._association_name

    def get_association_cardinality_min(self):
        return self._association_cardinality_min

    def get_association_cardinality_max(self):
        return self._association_cardinality_max
