from app.core.constants import Constants

class View:

    def __init__(self, table_name, column_name):
        self._table_name = table_name
        self._column_name = column_name
    
    def __str__(self):
        return self._table_name + Constants.DOT + self._column_name

    def get_table_name(self):
        return self._table_name

    def get_column_name(self):
        return self._column_name
