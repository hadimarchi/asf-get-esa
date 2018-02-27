# master.py
# master of child processes in children class
# Author: Hal DiMarchi
from contextlib import suppress
from copy import deepcopy
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

    def get_products_from_db(self):
        self.products = self.sql.get_granules()
        for product in range(len(self.products)):
            self.products[product] = get_product_from_url(
                                        self.products[product]
                                        )
            print(self.products[product])

    def reset_products_not_downloaded(self):
        log.debug(" cleaning up failed products ")
        log.debug(self.failed_products)
        log.debug("a failed product is {}".format(self.failed_products[0][0]))
        error = ""
        while self.failed_products:
            try:
                self.sql.cleanup(self.failed_products)
            except (Exception, BaseException, KeyboardInterrupt) as e:
                if str(e) != error:
                    log.debug(str(e))
                    error = str(e)
                continue
            else:
                log.debug("cleaned {}" .format(self.failed_products))
                self.failed_products = []

    def run(self):
        self.children.submitted_processes = len(self.products)
        self.failed_products = deepcopy(self.products)
        log.debug("products to get {}".format(self.failed_products))
        while self.products:
            log.debug("Running another {} products".format(len(self.products)))
            with suppress(Exception, BaseException, KeyboardInterrupt):
                count = min(self.options.max_processes,
                            len(self.products),
                            len(self.options.usernames))
                count_products = self.products[0:count]
                del self.products[0:count]
                log.debug("failed products should be the same {}".format(self.failed_products))
                difference = (count_products - (self.children.run(count_products)))
                log.debug("successful products were {}".format(difference))
                self.failed_products -= difference

        log.debug("products to be deleted  {}".format(self.failed_products))
        log.debug("waiting")
        while True:
            with suppress(Exception, BaseException, KeyboardInterrupt):
                while self.children.alive:
                    with suppress(Exception, BaseException, KeyboardInterrupt):
                        continue
                break

        log.debug("done waiting")
        while True:
            with suppress(Exception, BaseException, KeyboardInterrupt):
                while self.failed_products:
                    print(self.failed_products)
                    with suppress(Exception, BaseException, KeyboardInterrupt):
                        log.debug("products have not been scrubbed")
                        self.reset_products_not_downloaded()
                break
