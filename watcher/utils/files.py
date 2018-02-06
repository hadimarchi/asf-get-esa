# files.py
# Author: Hal DiMarchi
# File path and parsing setup for watcher

from bs4 import BeautifulSoup
import os


class Files():
    def __init__(self, watcher_path, log):
        self.name = 'esa_watcher'
        self.watcher_path = watcher_path
        self.log = log
        self.config_path = os.path.abspath(os.path.join(self.watcher_path, "config"))
        self.config = os.path.join(self.config_path, self.name + '.cfg')
