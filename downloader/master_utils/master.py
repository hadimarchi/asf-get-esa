# master.py
# master of child processes in children class
# Author: Hal DiMarchi
from copy import deepcopy
from time import sleep as wait
import signal
import sys

from . import check_and_clean_log_file, get_product_from_url, logging as log
from .children import Children
from .sql import Esa_Data_Sql
from .options import Options
from utils.error import KeyboardInterruptError


class Master:
    def __init__(self, location):
        self.options = Options(location)
        self.sql = Esa_Data_Sql(self.options)
        self.children = Children(sql=self.sql,
                                 max_processes=self.options.max_processes,
                                 usernames=self.options.usernames)
        self.register_signals()

    def register_signals(self):
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signal_number, stack_frame):
        sys.exit(0)

    def get_product_ids_from_url(self):
        for product in range(len(self.products)):
            self.products[product] = get_product_from_url(
                                        self.products[product])

    def get_products_from_db(self):
        self.products = self.sql.get_granules()
        self.children.submitted_processes = len(self.products)
        self.get_product_ids_from_url()

        log.info('Found {} products for this run.'.format(len(self.products)))
        log.info("Products for this run: {}".format(self.products))

    def reset_products_not_downloaded(self):
        try:
            log.info("Reseting failed products downloaded status to false.")
            log.error("Number of failed products: {}".format(len(self.failed_products)))

            self.sql.cleanup(self.failed_products)
            log.info("Reset failed_products.")
        except Exception:
            log.error("An error occurred with the database. Retrying reset")
            try:
                self.sql.cleanup(self.failed_products)

            except Exception as e:
                log.error("Granules could not be reset, download status in database may be innaccurate for some granules")
                log.error("Error was: {}".format(str(e)))
            else:
                log.error("Reset retry successful")

        except KeyboardInterrupt:
            log.info("Keyboard interrupt ignored. Need to reset failed products in db")
            self.reset_products_not_downloaded()

    def get_failed_products(self):
        log.info("Number of successfully downloaded products: {}".format(len(self.children.successful_granules_list)))
        self.failed_products = [product for product in self.failed_products if
                                product not in self.children.successful_granules_list]

    def download_products(self):
        try:
            self.failed_products = deepcopy(self.products)
            log.info("Number of products to download: {}".format(len(self.failed_products)))

            self.children.get_children_and_manager()
            self.children.run(self.products)

        except (KeyboardInterruptError, KeyboardInterrupt):
            log.info("Received keyboard interrupt, cleaning up and shutting down")
            sys.exit(0)

        except OSError as e:
            log.error("An operating system error occurred: {}".format(str(e)))
            sys.exit(0)

        except Exception as e:
            log.error("An error occurred: {} ".format(str(e)))

        finally:
            try:
                self.get_failed_products()
            except (BaseException, Exception):
                log.error("Failed products list is not accurate, some products may undergo an erroneous reset")
            finally:
                self.children.manager.shutdown()
                self.reset_products_not_downloaded()
                self.failed_products = []

    def idle(self):
        try:
            while self.options.run:
                check_and_clean_log_file()
                log.info("Spinning up download cycle")
                self.get_products_from_db()
                if self.products:
                    self.download_products()
                else:
                    wait(self.options.wait_period)
                self.options.update_max_processes_and_run()
            log.info("run option is not 1, exiting")
        finally:
            self.options.set_running('0')
