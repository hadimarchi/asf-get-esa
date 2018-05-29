# sql.py
# Author: Hal DiMarchi
# sql operations for esa_watcher
from . import log
import psycopg2

from importlib.machinery import SourceFileLoader as load
sql = load("share.options", "../shared/sql.py").load_module()


class Esa_Sql(sql.Sql):
    def __init__(self, options):
        super().__init__(options)
        self.get_connections()

    def get_connections(self):
        self.hyp3_db_connection = psycopg2.connect(self.options.hyp3_db)
        self.pg_db_connection = psycopg2.connect(self.options.pg_db)
        self.esa_data_db_connection = psycopg2.connect(self.options.esa_data_db)

        self.hyp3_db_connection.autocommit = True
        self.pg_db_connection.autocommit = True
        self.esa_data_db_connection.autocommit = True

    def do_hyp3_sql(self, sql, vals):
        return self.do_sql(self.hyp3_db_connection, sql, vals)

    def do_pg_sql(self, sql, vals):
        return self.do_sql(self.pg_db_connection, sql, vals)

    def do_esa_data_sql(self, sql, vals):
        return self.do_sql(self.esa_data_db_connection, sql, vals)

    def check_pg_db_for_product(self, product):
        query = self.do_pg_sql(self.options.find_granules_in_pg_sql,
                               {'name': product})
        return len(query)

    def check_hyp3_db_for_intersecting_subscription(self, product):
        try:
            intersecting_subscriptions = self.do_hyp3_sql(
                                         self.options.intersects_hyp3_subs_sql.format(
                                            self.options.users),
                                         product)
        except Exception:
            return False

        if intersecting_subscriptions:
            log.info(f"{product['identifier']} matched hyp3 subscriptions")
            log.info(f"subscriptions matching: {intersecting_subscriptions}")
            return True
        return False

    def insert_product_in_db(self, product):
        try:
            self.do_esa_data_sql(self.options.insert_sql, product)
        except psycopg2.IntegrityError as e:
            log.info("ESA database did not accept product")
            log.info("Reason: {}".format(str(e)))
        else:
            log.info("Inserted {}".format(product))

    def close_connections(self):
        self.hyp3_db_connection.close()
        self.pg_db_connection.close()
        self.esa_data_db_connection.close()
