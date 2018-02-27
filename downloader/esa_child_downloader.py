# esa_downloader
# Author: Hal DiMarchi
# Downloads high interest products from ESA as determined by esa_watcher.py
import logging
import os
from utils import downloader, options, error

logging.basicConfig(level=logging.DEBUG,
                    format='%(pathname)s %(asctime)s %(levelname)s %(message)s')


def download(granule_username):
    try:
        granule = granule_username[0][0]
        product = granule_username[0][1]
        username = granule_username[1]
        logging.info("Spinning up")
        child_options = options.Options(os.path.dirname(__file__), username)
        child_downloader = downloader.Downloader(os.path.dirname(__file__),
                                                 logging
                                                 )

        child_downloader.get_options(child_options)
        child_downloader.get_sentinel_api()
        child_downloader.get_download_path()

        child_downloader.download_granule(product=product, granule=granule)
        logging.info("Done")

    except (Exception, KeyboardInterrupt, BaseException, SystemExit):
        logging.error("Downloading of {} Failed, returning".format(granule))
        raise error.DownloadError(granule)
