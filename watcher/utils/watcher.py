from . import check_and_clean_log_file, get_product_dict, logging as log
from .sql import Esa_Sql
from .options import Options

from datetime import datetime
from sentinelsat.sentinel import SentinelAPI


class Watcher:
    def __init__(self, location):
        self.options = Options(location)
        self.sql = Esa_Sql(self.options)
        self.api = SentinelAPI(self.options.user, self.options.password)
        self.products = []

        check_and_clean_log_file()

    def find_candidate_products(self):
        log.info("Finding candidate products at ESA")
        self.candidate_products = self.api.query(limit=self.options.num_back,
                                                 producttype="SLC",
                                                 ingestiondate=(f"{self.options.last_search_time}Z",
                                                                datetime.isoformat(datetime.now())+"Z"))
        self.candidate_products.update(self.api.query(limit=self.options.num_back,
                                                      producttype="GRD",
                                                      ingestiondate=(f"{self.options.last_search_time}Z",
                                                                     datetime.isoformat(datetime.now())+"Z")))
        self.options.update_last_search_time()
        log.info("Inspecting {} products".format(len(self.candidate_products)))

    def filter_for_unknown_products(self):
        for product in self.candidate_products:
            if not self.sql.check_pg_db_for_product(
                    self.candidate_products[product]['identifier']):
                self.products.append(
                    (self.candidate_products[product]['identifier'],
                     self.candidate_products[product]['link_icon'],
                     self.candidate_products[product]['footprint'])
                    )
                log.info("{} is unknown to ASF".format(
                        self.candidate_products[product]['identifier']))

    def filter_for_subscription_intersection(self):
        for product in self.products:
            if not self.sql.check_hyp3_db_for_intersecting_subscription(product):
                log.info("{} did not match any Hyp3 subscriptions".format(product[0]))
                self.products.remove(product)

    def insert_products_in_db(self):
        for product in self.products:
            self.sql.insert_product_in_db(get_product_dict(product))
