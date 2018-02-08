# esa_downloader
# Author: Hal DiMarchi
# Downloads high interest products from ESA as determined by esa_watcher.py

import logging
import os
from utils import downloader, options, sql

logging.basicConfig(level=logging.DEBUG,
                    format='%(pathname)s %(asctime)s %(levelname)s %(message)s')


def get_granule_from_esa_data(sql):
    granule, url = sql.get_granule()
    return granule, url


def download():
    logging.info("Spinning up")
    child_options = options.Options(os.path.dirname(__file__))
    child_sql = sql.Esa_Data_Sql(child_options)
    child_downloader = downloader.Downloader(os.path.dirname(__file__),
                                             logging, child_sql
                                             )

    child_downloader.get_options(child_options)
    child_downloader.get_sentinel_api()
    child_downloader.get_download_path()

    granule, url = get_granule_from_esa_data(child_sql)

    child_downloader.download_granule(url=url, granule=granule)
    logging.info("Done")


if __name__ == "__main__":
    download()
