# esa_downloader
# Author: Hal DiMarchi
# Downloads high interest products from ESA as determined by esa_watcher.py
import os
from utils import downloader, options, logging as log
from utils.error import KeyboardInterruptError


class Child_Downloader:
    def __init__(self, args):
        self.granules = args["granules"]
        self.username = args["username"]
        self.successful_granules = args["successful_granules"]
        child_options = options.Options(os.path.dirname(__file__), self.username)
        self.downloader = downloader.Downloader(os.path.dirname(__file__), child_options)
        log.info('processing {} granules'.format(len(self.granules)))

    def download(self):
        try:
            for granule, product in self.granules:
                self.download_single_granule(granule, product)
        except KeyboardInterrupt:
            raise KeyboardInterruptError()

    def download_single_granule(self, granule, product):
        try:
            log.info("Spinning up single download")
            self.downloader.download_granule(granule=granule, product=product)
            log.info("Done")
        except OSError as e:
            raise e
        except Exception as e:
            log.error("Downloading of {} failed".format(granule))
            log.error("Error was: {}".format(str(e)))
        else:
            log.info("{} was successfully downloaded".format(granule))
            self.successful_granules.append((granule, product))
