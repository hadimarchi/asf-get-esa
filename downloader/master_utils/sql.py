# sql.py
# class for connecting with esa_data
# Author: Hal DiMarchi

from . import log

try:
    import psycopg2
except ImportError:
    import psycopg2cffi as psycopg2

from importlib.machinery import SourceFileLoader as load
sql = load("share.options", "../shared/sql.py").load_module()


class Esa_Data_Sql(sql.Sql):
    def __init__(self, options):
        super().__init__(options)
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
            products = self.do_sql(self.esa_data_db_connection,
                                   self.options.get_granule_from_esa_data)
        except Exception as e:
            log.error("Could not get granules.")
            log.error("Error was: {}".format(str(e)))
        else:
            self.do_multiple_updates(self.esa_data_db_connection,
                                     True,
                                     self.options.update_downloaded_for_esa_data,
                                     products)

        return products

    def cleanup(self, failed_products):
        log.info("Reseting granules")
        self.do_multiple_updates(self.esa_data_db_connection,
                                 False,
                                 self.options.update_downloaded_for_esa_data,
                                 failed_products)
