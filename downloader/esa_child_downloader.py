# esa_downloader
# Author: Hal DiMarchi
# Downloads high interest products from ESA as determined by esa_watcher.py
import os
from utils import downloader, options, logging as log
from utils.error import KeyboardInterruptError


def download(granules_username_list):
    try:
        granules = granules_username_list[0]
        username = granules_username_list[1]
        successful_granules = granules_username_list[2]

        log.info('processing {} granules'.format(len(granules)))
        for granule in granules:
            try:
                log.info("Spinning up single download")
                child_options = options.Options(os.path.dirname(__file__), username)
                child_downloader = downloader.Downloader(os.path.dirname(__file__))

                child_downloader.get_options(child_options)
                child_downloader.get_sentinel_api()
                child_downloader.get_download_path()
                child_downloader.download_granule(product=granule[1], granule=granule[0])
                log.info("Done")

            except Exception as e:
                log.error("Downloading of {} failed".format(granule))
                log.error("Error was: {}".format(str(e)))
            else:
                log.info("{} was successfully downloaded".format(granule))
                successful_granules.append(granule)
                log.debug("{}".format(successful_granules))
    except KeyboardInterrupt:
        raise KeyboardInterruptError()
