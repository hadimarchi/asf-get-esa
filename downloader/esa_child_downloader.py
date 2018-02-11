# esa_downloader
# Author: Hal DiMarchi
# Downloads high interest products from ESA as determined by esa_watcher.py

import logging
import os
from utils import downloader, options, error

logging.basicConfig(level=logging.DEBUG,
                    format='%(pathname)s %(asctime)s %(levelname)s %(message)s')


def download(product, granule):
    try:

        logging.info("Spinning up")
        child_options = options.Options(os.path.dirname(__file__))
        child_downloader = downloader.Downloader(os.path.dirname(__file__),
                                                 logging
                                                 )

        child_downloader.get_options(child_options)
        child_downloader.get_sentinel_api()
        child_downloader.get_download_path()

        child_downloader.download_granule(product=product, granule=granule)
        logging.info("Done")

    except Exception:
        raise error.DownloadError(granule)
