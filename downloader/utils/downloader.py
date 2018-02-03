# files.py
# Author: Hal DiMarchi
# File path setup for downloader

import os
from sys import exit
from sentinelsat.sentinel import SentinelAPI
from . import get_product_from_granule_url


class Downloader():
    def __init__(self, downloader_path, log):
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

    def download_granule(self, url, granule):
        product = get_product_from_granule_url(url)
        print(product)
        try:
            self.api.download(product, directory_path=self.download_path)

        except Exception as e:
            print(str(e))
            print("here we would change the download column of the db back to false")
            exit("Failed to download granule: {}".format(granule))
        else:
            print("here we would leave the db alone, or in the future change pending to done")
