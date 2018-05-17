# error.py
# errors class for esa_downloader
# Author: Hal Dimarchi


class DownloadError(Exception):
    def __init__(self, granule):
        self.granule = granule


class KeyboardInterruptError(Exception):
    pass
