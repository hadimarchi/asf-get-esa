# children.py
# wrapper around collection of children
# represented as processes

from . import logging as log
import esa_child_downloader as downloader
from multiprocessing import Pool
from multiprocessing.managers import SyncManager
import signal


def run_child(granule_username):
    return downloader.download(granule_username)


class Children:
    def __init__(self, sql, max_processes, usernames):
        self.sql = sql
        self.max_processes = max_processes
        self.usernames = usernames
        self.successful_granules = []

    def set_manager_to_survive_interrupt(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def get_children_and_manager(self):
        self.children = Pool(processes=self.max_processes)
        self.manager = SyncManager()
        self.manager.start(self.set_manager_to_survive_interrupt)
        self.successful_granules_list = self.manager.list(self.successful_granules)

    def generate_granule_username_pairing(self):
        if self.max_processes < self.product_count:
            chunk, remainder = divmod(self.product_count, self.max_processes)
            granules_usernames_list = [(self.products[i*chunk: (i+1)*chunk],
                                        self.usernames[i],
                                        self.successful_granules_list)
                                       for i in range(self.max_processes)]

            del self.products[self.max_processes*chunk]

            if remainder:
                for i in range(remainder):
                    granules_usernames_list[i][0].append(self.products[i])

        else:
            granules_usernames_list = [([self.products[i]],
                                        self.usernames[i],
                                        self.successful_granules_list)
                                       for i in range(self.product_count)]

        return granules_usernames_list

    def start_children(self, granules_usernames_list):
        self.children.map_async(run_child, granules_usernames_list)

    def join_children(self):
        self.children.close()
        self.children.join()

    def terminate_children(self):
        self.children.terminate()
        self.children.join()

    def run(self, products):
        self.products = products
        self.product_count = len(self.products)
        granules_usernames_list = self.generate_granule_username_pairing()
        log.info("granules/username pairs: {}".format(granules_usernames_list[:2]))
        try:
            self.start_children(granules_usernames_list)
            self.join_children()
        except (KeyboardInterrupt, Exception) as e:
            self.terminate_children()
            raise e
        else:
            log.info("finished downloading {} products".format(self.product_count))
