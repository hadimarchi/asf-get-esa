# esa_downloader
# Author: Hal DiMarchi
# Downloads high interest products from ESA as determined by esa_watcher.py
import os
from time import sleep
from utils import downloader, options, error, logging as log


def download(granules_username_queue):
    successful_granules = []
    granules = granules_username_queue[0]
    username = granules_username_queue[1]
    queue = granules_username_queue[2]
    log.info('processing {} granules'.format(len(granules)))
    for granule in granules:
        try:
            log.info("Spinning up single download")
            child_options = options.Options(os.path.dirname(__file__), username)
            child_downloader = downloader.Downloader(os.path.dirname(__file__))

            child_downloader.get_options(child_options)
            child_downloader.get_sentinel_api()
            child_downloader.get_download_path()

            # queue.put(child_downloader.download_granule(product=granule[1], granule=granule[0]))
            queue.put(1)
            sleep(2)
            log.info("Done")

        except Exception as e:
            log.error("Downloading of {} Failed, returning".format(granule))
            log.error("Error was: {}".format(str(e)))
        else:
            successful_granules.append(granule)
