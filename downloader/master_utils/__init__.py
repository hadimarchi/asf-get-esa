# __init__.py for
# master_utils module
# Author: Hal DiMarchi

import logging
import sys
import os


MAX_LOG_FILE_SIZE = 1000000
LOG_FILE_NAME = 'master.log'

logging.basicConfig(filename=LOG_FILE_NAME,
                    level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s')

log = logging.getLogger(__file__)


def add_sys_out_handler_to_log():
    log.addHandler(logging.StreamHandler(sys.stdout))


def get_product_from_url(product):
    url = product[1]
    granule = product[0]
    url = url.replace("https://scihub.copernicus.eu/apihub/odata/v1/Products('", '')
    url = url.replace(")/Products('Quicklook')", '')
    return (granule, url.replace("'/$value", ''))


def check_and_clean_log_file():
        log_file = os.open(LOG_FILE_NAME, os.O_APPEND)
        log_file_size = os.fstat(log_file).st_size
        logging.info("log is currently {} bytes".format(log_file_size))
        if log_file_size > (MAX_LOG_FILE_SIZE):
            with open(LOG_FILE_NAME, 'w'):
                pass
            logging.info("Cleaned log")
