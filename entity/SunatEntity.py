class SunatEntity(object):
    def __init__(self, id, table_name, locked, rows, last_update):
        self.id=id
        self.table_name=table_name
        self.locked=locked
        self.rows=rows
        self.last_update=last_update

    def __str__(self):
        return '{id="%s", table_name="%s", locked="%s", rows="%s", last_update="%s"}' % (self.id, 
            self.table_name, self.locked, self.rows, self.last_update)