from app.core.constants import Constants

class Rule:
    def __init__(self, table_name, column_name, comaprison_operator, value):
        self._table_name = table_name
        self._column_name = column_name
        self._comaprison_operator = getattr(Constants, comaprison_operator)
        self._value = value
    
    def __str__(self):
        return self._table_name + Constants.DOT + self._column_name + \
            Constants.SPACE + self._comaprison_operator + Constants.SPACE + \
            str(self._value) + Constants.SPACE
    
    def get_table_name(self):
        return self._table_name

    def get_column_name(self):
        return self._column_name

    def get_comaprison_operator(self):
        return self._comaprison_operator

    def get_value(self):
        return self._value