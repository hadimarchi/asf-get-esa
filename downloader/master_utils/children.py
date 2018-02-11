# children.py
# wrapper around collection of children
# represented as processes
import esa_child_downloader as downloader
from utils.error import DownloadError
from multiprocessing import Pool, Process


def run_child(product):
    downloader.download(granule=product[0], product=product[1])


class Children:
    def __init__(self, sql, max_processes):
        self.sql = sql
        self.failed_granules = []
        pass

    def add_child(self):
        pass

    def check_children(self):
        pass

    def remove_child(self):
        pass

    def run(self, products):
        try:
            self.children = Pool(processes=len(products), maxtasksperchild=1)
            self.children.map_async(run_child, products,
                                    error_callback=self.cleanup)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            self.children.terminate()
            print(str(e))
        else:
            self.children.close()
        finally:
            self.children.join()
            return self.failed_granules

    def cleanup(self, value):
        print("I am {}".format(str(value)))
        self.failed_granules.append(value)
