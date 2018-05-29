# sql.py
# class for connecting with esa_data
# Author: Hal DiMarchi

from . import log

try:
    import psycopg2
except ImportError:
    import psycopg2cffi as psycopg2


class Esa_Data_Sql:
    def __init__(self, options):
        self.options = options
        self.get_connections()

    def get_connections(self):
        try:
            self.esa_data_db_connection = psycopg2.connect(self.options.esa_data_db)
            self.esa_data_db_connection.autocommit = True
        except Exception as e:
            log.error(str(e))
            self.options.set_running('0')
            raise e

    def close_connections(self):
        self.esa_data_db_connection.close()

    def get_granules(self):
        try:
            products = do_sql(self.esa_data_db_connection,
                              self.options.get_granule_from_esa_data)
        except Exception as e:
            log.error("Could not get granules.")
            log.error("Error was: {}".format(str(e)))
        else:
            do_multiple_updates(self.esa_data_db_connection,
                                True,
                                self.options.update_downloaded_for_esa_data,
                                products)

        return products

    def cleanup(self, failed_products):
        log.info("Reseting granules")
        do_multiple_updates(self.esa_data_db_connection,
                            False,
                            self.options.update_downloaded_for_esa_data,
                            failed_products)


def do_sql(db_conn, sql, vals=None):
    cur = db_conn.cursor()
    cur.execute(sql, vals) if vals else cur.execute(sql)
    try:
        res = cur.fetchall()
    except Exception:
        cur.close()
        return ""
    cur.close()
    return res


def do_multiple_updates(db_conn, true_false, sql, products):
    cur = db_conn.cursor()
    for product in range(len(products)):
        vals = {'true_false': true_false,
                'granule': products[product][0]}
        cur.execute(sql, vals)
    cur.close()
