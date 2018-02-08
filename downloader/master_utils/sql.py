# sql.py
# class for connecting with esa_data
# Author: Hal DiMarchi

try:
    import psycopg2
except ImportError:
    import psycopg2cffi as psycopg2


class Esa_Data_Sql:
    def __init__(self, options):
        self.options = options
        self.get_connections()

    def get_connections(self):
        self.esa_data_db_connection = psycopg2.connect(self.options.esa_data_db)
        self.esa_data_db_connection.autocommit = True

    def get_granules(self):
        try:
            products = do_sql(self.esa_data_db_connection,
                              self.options.get_granule_from_esa_data)
            print(products)
        except Exception as e:
            print(str(e))

        else:
            pass
            # alert db

        return products


def do_sql(db_conn, sql, vals=None):
    cur = db_conn.cursor()
    cur.execute(sql, vals) if vals else cur.execute(sql)
    try:
        res = cur.fetchall()
    except:
        cur.close()
        return ""

    cur.close()
    return res
