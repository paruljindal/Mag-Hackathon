class ObjectModel:
    def __init__(self, views, joins, conditions):
        self._views = views
        self._joins = joins
        self._conditions = conditions

    def get_joins(self):
        return self._joins

    def get_views(self):
        return self._views

    def get_conditions(self):
        return self._conditions
