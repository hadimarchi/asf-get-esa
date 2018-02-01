# sql.py
# Author: Hal DiMarchi
# sql operations for esa_watcher

try:
    import psycopg2
except Exception:
    import psycopg2cffi as psycopg2


class Esa_Sql():
    def __init__(self, options):
        self.get_connections(options)

    def get_connections(self, options):
        self.hyp3_db_connection = psycopg2.connect(options.hyp3_db)
        # self.pg_db_connection = psycopg2.connect(options.pg_db)
        self.esa_data_db_connection = psycopg2.connect(options.esa_data_db)

        self.hyp3_db_connection.autocommit = True
        # self.pg_db_connection.autocommit = True
        self.esa_data_db_connection.autocommit = True

    def do_hyp3_sql(self, sql, vals):
        return do_sql(self.hyp3_db_connection, sql, vals)

    def do_pg_sql(self, sql, vals):
        return do_sql(self.pg_db_connection, sql, vals)

    def do_esa_data_sql(self, sql, vals):
        return do_sql(self.esa_data_db_connection, sql, vals)

    def close_connections(self):
        self.hyp3_db_connection.close()
        # self.pg_db_connection.close()
        self.esa_data_db_connection.close()


def do_sql(db_conn, sql, vals):
    cur = db_conn.cursor()
    cur.execute(sql, vals)

    try:
        res = cur.fetchall()
    except:
        res = ""

    db_conn.commit()
    cur.close()
    return res
