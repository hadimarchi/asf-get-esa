# sql.py
# Author: Hal DiMarchi
# sql operations for esa_downloader

try:
    import psycopg2
except Exception:
    import psycopg2cffi as psycopg2


class Esa_Data_Sql():
    def __init__(self, options):
        self.options = options
        self.get_connections()

    def get_connections(self):
        self.esa_data_db_connection = psycopg2.connect(self.options.esa_data_db)
        self.esa_data_db_connection.autocommit = True

    def get_granule(self):
        try:
            granule, url = do_sql(self.esa_data_db_connection,
                                  self.options.get_granule_from_esa_data)
        except Exception as e:
            print(str(e))

        else:
            do_sql(self.esa_data_db_connection,
                   self.options.update_downloaded_for_esa_data,
                   {'granule': granule})

        return granule, url

    def close_connections(self):
        self.esa_data_db_connection.close()


def do_sql(db_conn, sql, vals=None):
    cur = db_conn.cursor()
    cur.execute(sql, vals) if vals else cur.execute(sql)
    try:
        res = cur.fetchall()
    except:
        cur.close()
        return ""

    cur.close()
    return res[0][0], res[0][1]
