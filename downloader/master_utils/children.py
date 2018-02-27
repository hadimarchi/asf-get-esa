# children.py
# wrapper around collection of children
# represented as processes

from . import logging as log
import esa_child_downloader as downloader
from utils.error import DownloadError
from contextlib import suppress
from multiprocessing import Pool, Process


def run_child(granule_username):
    return downloader.download(granule_username)


class Children:
    def __init__(self, sql, max_processes, usernames):
        self.sql = sql
        self.max_processes = max_processes
        self.submitted_processes = 0
        self.accomplised_processes = 0
        self.failed_granules = []
        self.usernames = usernames
        self.alive = True
        pass

    def add_child(self):
        pass

    def check_children(self):
        pass

    def remove_child(self):
        pass

    def run(self, products):
        process_count = len(products)
        granules_usernames = [(products[i], self.usernames[i]) for i in range(process_count)]
        self.children = Pool(processes=process_count,
                             maxtasksperchild=1)
        self.children.map_async(
                                run_child, granules_usernames,
                                error_callback=self.cleanup
                                )
        self.children.close()
        while True:
            with suppress(Exception, BaseException, KeyboardInterrupt):
                self.children.join()
                break

        log.debug("pool has finished")
        while True:
            with suppress(Exception, BaseException, KeyboardInterrupt):
                print(self.failed_granules)
                self.accomplised_processes += len(products)
                log.debug(" run through {}".format(self.accomplised_processes))
                self.check_done()
                return self.failed_granules

    def cleanup(self, value):
        while str(value) not in self.failed_granules:
            with suppress(Exception, BaseException, KeyboardInterrupt):
                print("I am {}".format(str(value)))
                self.failed_granules.append(str(value))
                print(self.failed_granules)

    def check_done(self):
        if self.accomplised_processes >= self.submitted_processes:
            self.alive = False
