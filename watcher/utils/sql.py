# sql.py
# Author: Hal DiMarchi
# sql operations for esa_watcher
from . import logging as log
try:
    import psycopg2
except Exception:
    import psycopg2cffi as psycopg2


class Esa_Sql():
    def __init__(self, options):
        self.options = options
        self.get_connections()

    def get_connections(self):
        log.info("Hyp3 connection is {}".format(self.options.hyp3_db))
        self.hyp3_db_connection = psycopg2.connect(self.options.hyp3_db)
        self.pg_db_connection = psycopg2.connect(self.options.pg_db)
        self.esa_data_db_connection = psycopg2.connect(self.options.esa_data_db)

        self.hyp3_db_connection.autocommit = True
        self.pg_db_connection.autocommit = True
        self.esa_data_db_connection.autocommit = True

    def do_hyp3_sql(self, sql, vals):
        return do_sql(self.hyp3_db_connection, sql, vals)

    def do_pg_sql(self, sql, vals):
        return do_sql(self.pg_db_connection, sql, vals)

    def do_esa_data_sql(self, sql, vals):
        return do_sql(self.esa_data_db_connection, sql, vals)

    def check_pg_db_for_product(self, product):
        query = self.do_pg_sql(self.options.find_granules_in_pg_sql,
                               {'name': product})
        print(query)
        return len(query)

    def check_hyp3_db_for_intersecting_subscription(self, location):
        try:
            self.do_hyp3_sql(
                             self.options.intersects_hyp3_subs_sql.format(
                                 self.options.users),
                             {'location': location})
        except:
            return False
        else:
            return True

    def insert_product_in_db(self, product):
        self.do_esa_data_sql(self.options.insert_sql, product)

    def close_connections(self):
        self.hyp3_db_connection.close()
        self.pg_db_connection.close()
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
