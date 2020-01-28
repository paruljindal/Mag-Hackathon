class QueryHolder:
    def __init__(self, query, alter_commands):
        self._query = query
        self._alter_commands = alter_commands

    def get_query(self):
        return self._query

    def get_alter_commands(self):
        return self._alter_commands
