# children.py
# wrapper around collection of children
# represented as processes

from . import logging as log
import esa_child_downloader as downloader
from utils.error import KeyboardInterruptError
from multiprocessing import Pool, Queue


def run_child(granule_username):
    return downloader.download(granule_username)


class Children:
    def __init__(self, sql, max_processes, usernames):
        self.sql = sql
        self.max_processes = max_processes
        self.usernames = usernames

    def get_children(self):
        self.children = Pool(processes=self.max_processes)

    def setup_and_run_children(self, granules_usernames):
        return self.children.map_async(run_child, granules_usernames)

    def run(self, products):
        self.products = products
        process_count = len(self.products)

        if self.max_processes < process_count:
            chunk, remainder = divmod(process_count, self.max_processes)
            successful_granules_queue = Queue()
            granules_usernames_queue = [(self.products[i*chunk: (i+1)*chunk],
                                        self.usernames[i], successful_granules_queue) for i in range(self.max_processes)]
            del self.products[self.max_processes*chunk]

            for i in range(remainder):
                granules_usernames_queue[i][0].append(self.products[i])

        else:
            granules_usernames_queue = [([self.products[i]], self.usernames[i], successful_granules_queue) for i in range(process_count)]

        log.info("granules/username pairs: {}".format(granules_usernames_queue[:2]))
        try:
            self.setup_and_run_children(granules_usernames_queue)

        except (Exception) as e:
            log.error("An error occurred: {} ".format(str(e)))
        else:
            log.info("finished downloading {} products".format(process_count))
        finally:
            while not successful_granules_queue.empty():
                self.successful_granules.append(self.successful_granules_queue.get())
