# files.py
# Author: Hal DiMarchi
# File path setup for downloader

import os
from sentinelsat.sentinel import SentinelAPI
from . import logging as log


class Downloader():
    def __init__(self, downloader_path):
        self.name = 'esa_downloader'
        self.downloader_path = downloader_path

    def get_options(self, options):
        self.options = options

    def get_download_path(self):
        self.download_path = os.path.abspath(os.path.join(
                                                self.downloader_path,
                                                self.options.download_dir
                                                    ))

        try:
            os.mkdir(self.download_path)
        except OSError:
            pass

    def get_sentinel_api(self):
        self.api = SentinelAPI(self.options.user, self.options.password,
                               self.options.esa_host)

    def download_granule(self, product, granule):
        log.info("Downloading product: {} corresponding to granule: {}"
                 .format(product, granule))
        self.api.download(product, directory_path=self.download_path)
