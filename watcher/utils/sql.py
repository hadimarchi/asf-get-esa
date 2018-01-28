# sql.py
# Author: Hal DiMarchi
# sql operations for esa_watcher

import psycopg2


class Esa_Sql():
    def __init__(self, options):
        self.get_connections(options)

    def get_connections(self, options):
        self.hyp3_db_connection = psycopg2.connect(options.hyp3_db)
        self.pg_db_connection = psycopg2.connect(options.pg_db)

        self.hyp3_db_connection.autocommit = True
        self.pg_db_connection.autocommit = True

    def do_hyp3_sql(self, sql, vals):
        return do_sql(self.hyp3_db_connection, sql, vals)

    def do_pg_sql(self, sql, vals):
        return do_sql(self.pg_db_connection, sql, vals)


def do_sql(db_conn, sql, vals):
    cur = db_conn.cursor()
    cur.execute(sql, vals)
    res = cur.fetchall()
    db_conn.commit()
    cur.close()
    return res
