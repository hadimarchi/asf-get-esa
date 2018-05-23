# children.py
# wrapper around collection of children
# represented as processes

from . import log
import esa_child_downloader as downloader
from multiprocessing import Pool
from multiprocessing.managers import SyncManager
import signal
import sys


def run_child(granules_username_list):
    child = downloader.Child_Downloader(granules_username_list)
    return child.download()


class Children:
    def __init__(self, sql, max_processes, usernames):
        self.sql = sql
        self.max_processes = max_processes
        self.usernames = usernames
        signal.signal(signal.SIGHUP, self.master_death_handler)

    def master_death_handler(self):
        self.children.terminate()
        log.error("Master died!")
        sys.exit(0)

    def set_manager_to_survive_interrupt_and_terminate(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)

    def get_children_and_manager(self):
        self.children = Pool(processes=self.max_processes)
        self.manager = SyncManager()
        self.manager.start(self.set_manager_to_survive_interrupt_and_terminate)
        self.successful_granules_list = self.manager.list()

    def generate_child_argument_dict_from_max_processes(self):
        chunk, remainder = divmod(self.product_count, self.max_processes)
        self.granules_usernames_list = [{"granules": self.products[i*chunk: (i+1)*chunk],
                                         "username": self.usernames[i],
                                         "successful_granules": self.successful_granules_list}
                                        for i in range(self.max_processes)]

        del self.products[:(self.max_processes*chunk)]
        for i in range(remainder):
            self.granules_usernames_list[i]["granules"].append(self.products[i])

    def generate_child_argument_dict_from_product_count(self):
        self.granules_usernames_list = [{"granules": [self.products[i]],
                                         "username": self.usernames[i],
                                         "successful_granules": self.successful_granules_list}
                                        for i in range(self.product_count)]

    def generate_child_arguments(self):
        if self.max_processes < self.product_count:
            self.generate_child_argument_dict_from_max_processes()

        else:
            self.generate_child_argument_dict_from_product_count()

    def start_children(self):
        self.children.map_async(run_child, self.granules_usernames_list)

    def join_children(self):
        self.children.close()
        self.children.join()

    def terminate_children(self):
        self.children.terminate()
        self.children.join()

    def run(self, products):
        self.products = products
        self.product_count = len(self.products)
        self.generate_child_arguments()
        log.debug("granules/username pairs: {}".format([(pair['granules'], pair['username']) for pair in self.granules_usernames_list]))
        try:
            self.start_children()
            self.join_children()
        except (KeyboardInterrupt, Exception) as e:
            self.terminate_children()
            raise e
        else:
            log.info("finished attempting to download {} products".format(self.product_count))
