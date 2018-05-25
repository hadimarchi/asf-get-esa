# files.py
# Author: Hal DiMarchi
# File path setup for downloader

from shutil import move
import os
from sentinelsat.sentinel import SentinelAPI
from . import ensure_paths, logging as log
from .sql import Hyp3_Archive_Sql


class Downloader():
    def __init__(self, downloader_path, options):
        self.downloader_path = downloader_path
        self.options = options
        self.hyp3_archive_db = Hyp3_Archive_Sql(self.options.pg_db,
                                                self.options.find_granule_sql)
        self.get_sentinel_api()
        self.get_download_path()
        ensure_paths([self.download_path, self.options.final_dir])

    def get_download_path(self):
        self.download_path = os.path.abspath(os.path.join(
                                                self.downloader_path,
                                                self.options.download_dir
                                                    ))

    def get_sentinel_api(self):
        self.api = SentinelAPI(self.options.user, self.options.password,
                               self.options.esa_host)

    def download_granule(self, product, granule):
        log.info(f"Downloading product: {product} corresponding to granule: {granule}")

        if not self.is_product_handled(product=product, granule=granule):
            self.api.download(product, directory_path=self.download_path)
            move(os.path.join(self.download_path, f"{granule}.zip"),
                 self.options.final_dir)

    def is_product_handled(self, product, granule):
        if not self.hyp3_archive_db.is_granule_in_hyp3(product):
            if not os.path.exists(os.path.join(self.options.final_dir, f"{granule}*")):
                return False

        log.info(f"Product {product} correspond to granule {granule} has already been handled")
        return True
