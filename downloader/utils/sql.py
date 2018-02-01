# sql.py
# Author: Hal DiMarchi
# sql operations for esa_downloader

try:
    import psycopg2
except Exception:
    import psycopg2cffi as psycopg2


class Esa_Data_Sql():
    def __init__(self, options):
        self.get_connections(options)

    def get_connections(self, options):
        self.esa_data_db_connection = psycopg2.connect(options.esa_data_db)
        self.esa_data_db_connection.autocommit = True

    def get_granule(self):
        granule, url = do_sql(self.esa_data_db_connection,
                              self.options.get_granule_from_esa_data)
        return granule, url

    def close_connections(self):
        self.esa_data_db_connection.close()


def do_sql(db_conn, sql):
    cur = db_conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    return res
