class Conditions:
    def __init__(self, logical_operator, rules):
        self._logical_operator = logical_operator
        self._rules = rules
    
    def get_logical_operator(self):
        return self._logical_operator

    def get_rules(self):
        return self._rules