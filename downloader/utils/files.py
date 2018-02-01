# files.py
# Author: Hal DiMarchi
# File path setup for downloader

import os
import wget
from . import execute


class Files():
    def __init__(self, downloader_path, download_dir, log):
        self.name = 'esa_downloader'
        self.downloader_path = downloader_path
        self.download_dir = os.path.abspath(os.path.join(
                                                self.downloader_path,
                                                download_dir
                                                    ))

        self.config_path = os.path.abspath(os.path.join(self.watcher_path, "config"))
        self.config = os.path.join(self.config_path, self.name + '.cfg')

    def make_granule_path(self, granule):
        self.granule_path = os.path.join(self.download_dir, granule + '.zip')

    def download_granule(url, granule):
        wget.download(url, out=self.make_granule_path(granule))
