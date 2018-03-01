# master.py
# master of child processes in children class
# Author: Hal DiMarchi
from contextlib import suppress
from copy import deepcopy
from time import sleep as wait

from . import get_product_from_url, logging as log
from .children import Children
from .sql import Esa_Data_Sql
from .options import Options


class Master:
    def __init__(self, location):
        self.options = Options(location)
        self.sql = Esa_Data_Sql(self.options)
        self.children = Children(self.sql,
                                 self.options.max_processes,
                                 self.options.usernames)

    def get_product_ids_from_url(self):
        for product in range(len(self.products)):
            self.products[product] = get_product_from_url(
                                        self.products[product]
                                        )

    def get_products_from_db(self):
        self.products = self.sql.get_granules()
        self.children.submitted_processes = len(self.products)
        self.get_product_ids_from_url()

        log.info('Found {} products for this run.'.format(len(self.products)))
        log.info("Products for this run: {}".format(self.products))

    def reset_products_not_downloaded(self):
        log.debug("Reseting failed products.")
        while self.failed_products:
            try:
                self.sql.cleanup(self.failed_products)
            except (Exception, BaseException, KeyboardInterrupt) as e:
                continue
            else:
                log.debug("Reset failed_products.")
                self.failed_products = []

    def run(self):
        self.failed_products = deepcopy(self.products)
        log.debug("Products to get: {}".format(self.failed_products))
        while self.products:
            with suppress(Exception, BaseException, KeyboardInterrupt):
                count = min(self.options.max_processes,
                            len(self.products),
                            len(self.options.usernames))
                count_products = self.products[0:count]
                del self.products[0:count]
                difference = (count_products - (self.children.run(count_products)))
                self.failed_products -= difference

        log.debug("Products to be reset in db: {}".format(self.failed_products))
        self.reset_products_not_downloaded()

    def idle(self):
        while self.options.run:
            with suppress(Exception, BaseException, KeyboardInterrupt):
                self.get_products_from_db()
                self.run() if self.products else wait(self.options.wait_period)
                self.options.update_max_processes_and_run()
