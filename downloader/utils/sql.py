import psycopg2

from importlib.machinery import SourceFileLoader as load
sql = load("share.options", "../shared/sql.py").load_module()


class Hyp3_Archive_Sql(sql.Sql):
    def __init__(self, connection_string, check_granules_sql):
        self.connection_string = connection_string
        self.check_granules_sql = check_granules_sql
        self.get_archive_connection()

    def get_archive_connection(self):
        self.archive_connection = psycopg2.connect(self.connection_string)

    def is_granule_in_hyp3(self, product):
        exists = self.do_sql(self.archive_connection,
                             self.check_granules_sql,
                             {"name": product})
        return len(exists)
