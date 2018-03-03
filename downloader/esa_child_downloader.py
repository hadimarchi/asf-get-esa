# esa_downloader
# Author: Hal DiMarchi
# Downloads high interest products from ESA as determined by esa_watcher.py
import os
from utils import downloader, options, error, logging as log


def download(granule_username):
    try:
        granule = granule_username[0][0]
        product = granule_username[0][1]
        username = granule_username[1]
        log.info("Spinning up")
        child_options = options.Options(os.path.dirname(__file__), username)
        child_downloader = downloader.Downloader(os.path.dirname(__file__))

        child_downloader.get_options(child_options)
        child_downloader.get_sentinel_api()
        child_downloader.get_download_path()

        child_downloader.download_granule(product=product, granule=granule)
        log.info("Done")

    except (Exception, KeyboardInterrupt, BaseException, SystemExit) as e:
        log.error("Downloading of {} Failed, returning".format(granule))
        log.error("Error was: {}".format(str(e)))
        raise error.DownloadError(granule)
