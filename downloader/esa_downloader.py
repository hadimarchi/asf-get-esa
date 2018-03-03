# esa_downloader
# Author: Hal DiMarchi
# Downloads high interest products from ESA as determined by esa_watcher.py

import logging
import os
from utils import execute, downloader, options, sql

logging.basicConfig(level=logging.DEBUG,
                    format='%(pathname)s %(asctime)s %(levelname)s %(message)s')


def get_granule_from_esa_data():
    granule, url = sql.get_granule()
    return granule, url


if __name__ == "__main__":
    logging.info("Spinning up")
    options = options.Options(os.path.dirname(__file__))
    sql = sql.Esa_Data_Sql(options)
    downloader = downloader.Downloader(os.path.dirname(__file__), logging, sql)

    downloader.get_options(options)
    downloader.get_sentinel_api()
    downloader.get_download_path()

    granule, url = get_granule_from_esa_data()

    downloader.download_granule(url=url, granule=granule)
    logging.info("Done")
