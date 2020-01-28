class Rules:
    def __init__(self, rule, conditions):
        self._rule = rule
        self._conditions = conditions

    def get_rule(self):
        return self._rule

    def get_conditions(self):
        return self._conditions
    
    def add_condition(self, condition):
        self._conditions.append(condition)