from app.core.constants import Constants

class Joins:

    def __init__(self, left_table_name, right_table_name,
                 left_column_name, right_column_name, join_type):
        self._left_table_name = left_table_name
        self._right_table_name = right_table_name
        self._left_column_name = left_column_name
        self._right_column_name = right_column_name
        self._join_type = join_type

    def __str__(self):
        return self._left_table_name + Constants.SPACE + \
            self._join_type + Constants.SPACE + self._right_table_name  + \
            Constants.SPACE + \
            Constants.ON + Constants.SPACE + self._left_table_name + \
            Constants.DOT + self._left_column_name + Constants.SPACE +\
            Constants.EQ + Constants.SPACE + self._right_table_name + \
            Constants.DOT + self._right_column_name + \
            Constants.SPACE
        
        
        Constants.DOT + self._column_name

    def get_left_table_name(self):
        return self._left_table_name

    def get_left_column_name(self):
        return self._left_column_name

    def get_right_table_name(self):
        return self._right_table_name

    def get_right_column_name(self):
        return self._right_column_name

    def get_join_type(self):
        return self._join_type
