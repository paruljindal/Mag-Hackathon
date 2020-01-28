# from .association_model import AssociationModel
from app.core.constants import Constants
from app.core.helper import Helper


class QueryConverter:

    def __init__(self):
        self._output_file_object = {}
        self._query_object = {}
        self._views_object = {}
        self._joins_object = {}
        self._condition_object = {}

    # '''
    # Super Private Methods
    # '''

    # '''
    # Static Methods
    # '''

    # '''
    # Static Methods End
    # '''

    # '''
    # Super Private Methods End
    # '''

    # '''
    # Private Methods
    # '''

    '''
    Private Methods End
    '''

    def _handle_views(self):
        select_statement = Constants.SELECT + Constants.SPACE
        for view in self._views_objects:
            select_statement += view.__str__() \
                + Constants.COMMA + Constants.SPACE
        
        select_statement = select_statement[:-2] +  Constants.SPACE
        return select_statement
    
    
    def _handle_joins(self):
        join_statement = Constants.FROM + Constants.SPACE
        for join in self._joins_objects:
            join_statement += join.__str__()
        return join_statement
    
    def _handle_condition(self, conditions, flag_first = False):
        condition_statement = ""
        condition_bracket_flag = False
        if (len(conditions) >1):
            condition_bracket_flag = True
        
        for condition in conditions:
            if(not flag_first):
                condition_statement+= Constants.SPACE + \
                    condition.get_logical_operator() + Constants.SPACE
            
            if condition_bracket_flag:
                condition_statement += "(" 
            
            condition_statement += (condition.get_rules())[0].get_rule().__str__()
            condition_recursion = self._handle_condition((condition.get_rules())[0].get_conditions())
            if condition_recursion:
                condition_statement += condition_recursion
            
            if condition_bracket_flag:
                condition_statement+= ") "
        return condition_statement

    '''
    Public Methods
    '''

    def generate_query(self, object):
        self._query_object = object
        self._views_objects = object._views
        self._joins_objects = object._joins
        self._condition_object = (object._conditions)
        
        query_holder = ""
        query_holder += self._handle_views()
        query_holder += self._handle_joins()
        query_holder += Constants.WHERE + Constants.SPACE
        query_holder += self._handle_condition(self._condition_object, flag_first = True)
        
        return query_holder
