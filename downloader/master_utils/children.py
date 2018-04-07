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

    def cleanup(self, value):
        while str(value) not in self.failed_granules:
            with suppress(Exception, BaseException, KeyboardInterrupt):
                log.error("Failed Granule: {}".format(str(value)))
                self.failed_granules.append(str(value))

    def get_children(self, process_count, granules_usernames):
        log.debug("granule/username pairs again: {}".format(granules_usernames))
        self.children = Pool(processes=process_count)

    def set_children(self, granules_usernames):
        self.children.map_async(
                                run_child, granules_usernames,
                                error_callback=self.cleanup
                                )
        # self.children.close()

    def join_children(self):
        while True:
            with suppress(Exception, BaseException, KeyboardInterrupt):
                self.children.join()
                break

    def run(self, products):
        process_count = len(products)
        granules_usernames = [(products[i], self.usernames[i]) for i in range(process_count)]
        log.debug("granule/username pairs: {}".format(granules_usernames))
        self.set_children(granules_usernames)
        self.join_children()

        log.debug("finished downloading {} products".format(process_count-self.failed_granules))

        return self.failed_granules
