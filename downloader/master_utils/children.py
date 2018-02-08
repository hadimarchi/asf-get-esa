# children.py
# wrapper around collection of children
# represented as processes
import esa_child_downloader as downloader
from utils.error import DownloadError
from multiprocessing import Pool, Process


class Children:
    def __init__(self):
        self.children = []
        pass

    def add_child(self):
        pass

    def check_children(self):
        pass

    def remove_child(self):
        pass

    def run_child(self, child):
        downloader.download()
