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
        try:
            log.debug("Reseting failed products downloaded status to false.")
            log.info("Products to be reset in db: {}".format(self.failed_products))

            self.sql.cleanup(self.failed_products)
            log.debug("Reset failed_products.")
        except (Exception, BaseException):
            log.error("An error occurred in the database. Retrying reset")
            try:
                self.sql.cleanup(self.failed_products)
                log.info("Reset retry successful")
            except (Exception, BaseException):
                log.error("Granules could not be reset, download status in database may be innaccurate for some granules")
                log.error("Failed Products: {}".format(self.failed_products))

        except KeyboardInterrupt:
            log.info("Keyboard interrupt ignored. Need to reset failed products in db")
            self.reset_products_not_downloaded()

    def run(self):
        self.failed_products = deepcopy(self.products)
        log.info("Products to get: {}".format(self.failed_products))
        self.children.get_children()
        try:
            self.children.run(self.products)
            log.info("successful_products products were {}".format(self.children.successful_granules))

        except KeyboardInterrupt:
            log.info("Received keyboard interrupt, cleaning up and shutting down")
            self.options.run = 0

        finally:
            self.failed_products = [product for product in self.failed_products if (
                product not in self.children.successful_granules[i] for i in range(len(self.children.successful_granules)))]
            self.reset_products_not_downloaded()

    def idle(self):
        while self.options.run:
            log.info("Spinning up download cycle")
            self.get_products_from_db()
            if self.products:
                self.run()
            else:
                wait(self.options.wait_period)
                self.options.update_max_processes_and_run()
        log.info("run option is not 1, exiting")
