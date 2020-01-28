from .object_model import ObjectModel
from .joins import Joins
from .view import View
from .conditions import Conditions
from .rules import Rules
from .rule import Rule
from app.core.constants import Constants


class ConstructModel:
    def __init__(self):
        self._conditions = []
        self._views = []
        self._joins = []
        self._return_object = {}
        pass

    @staticmethod
    def __get_rule_object(rule):
        return Rule(rule[Constants.TABLE_NAME],
                    rule[Constants.COLUMN_NAME],
                    rule[Constants.COMPARISION_OPERATOR],
                    rule[Constants.VALUE])

    def _get_rules(self, rules):
        rules_objects = []
        for rule in rules:
            conditions = []
            if Constants.RULE in rule:
                rule_object = self.__get_rule_object(rule[Constants.RULE])
                if Constants.CONDITIONS in rule:
                    self._fill_object(rule[Constants.CONDITIONS], conditions)
                rules_objects.append(Rules(rule_object, conditions))
        return rules_objects

    @staticmethod
    def _fill_conditions(logical_operator, rules):
        return Conditions(logical_operator, rules)

    def _fill_object(self, condition_object, conditions):

        for condition in condition_object:
            if Constants.RULES in condition:
                conditions.append(self._fill_conditions(condition[Constants.LOGICAL_OPERATOR],
                                                        self._get_rules(condition[Constants.RULES])))
            else:
                conditions.append(self._fill_conditions(condition[Constants.LOGICAL_OPERATOR], []))

    def construct(self, views_object, joins_object, condition_object):
        self._views = []
        self._joins = []

        for view in views_object:
            view_model = View(view[Constants.TABLE_NAME],
                              view[Constants.COLUMN_NAME])
            self._views.append(view_model)

        for join in joins_object:
            join_model = Joins(
                join[Constants.LEFT_TABLE_NAME],
                join[Constants.RIGHT_TABLE_NAME],
                join[Constants.LEFT_COLUMN_NAME],
                join[Constants.RIGHT_COLUMN_NAME],
                join[Constants.JOIN_TYPE])
            self._joins.append(join_model)

        self._conditions = []
        self._fill_object(condition_object, self._conditions)
        # self._return_object = {"views" : self._views, "joins" : self._joins, "conditions" : self._conditions}
        return self
