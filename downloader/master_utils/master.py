# master.py
# master of child processes in children class
# Author: Hal DiMarchi

from . import get_product_from_url
from .children import Children
from .sql import Esa_Data_Sql
from .options import Options


class Master:
    def __init__(self, location):
        self.options = Options(location)
        self.sql = Esa_Data_Sql(self.options)
        self.children = Children(self.sql, self.options.max_processes)

    def get_products_from_db(self):
        self.products = self.sql.get_granules()
        for product in range(len(self.products)):
            self.products[product] = get_product_from_url(
                                        self.products[product]
                                        )
            print(self.products[product])

    def reset_products_not_downloaded(self, failed_granules):
        for granule in failed_granules:
            self.sql.cleanup(granule)

    def run(self):
        while self.products:
            try:
                count = min(self.options.max_processes, len(self.products))
                failed_granules = self.children.run(self.products[0:count])
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                incomplete = []
                for product in self.products[0:count]:
                    incomplete.append(product[0])
                self.reset_products_not_downloaded(incomplete)
            else:
                self.reset_products_not_downloaded(failed_granules)
            finally:
                del self.products[0:count]
