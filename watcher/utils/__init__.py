# __init__.py
# Author: Hal DiMarchi
# utils package for esa_watcher script

import logging
import sys
import os

MAX_LOG_FILE_SIZE = 500000
LOG_FILE_NAME = 'watcher.log'

logging.basicConfig(filename=LOG_FILE_NAME,
                    level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s')

log = logging.getLogger(__file__)


def add_sys_out_handler_to_log():
    log.addHandler(logging.StreamHandler(sys.stdout))


def get_product_dict(product):
    return {'granule': product[0],
            'url': product[1]}


def check_and_clean_log_file():
        log_file = os.open(LOG_FILE_NAME, os.O_APPEND)
        log_file_size = os.fstat(log_file).st_size
        logging.info("log is currently {} bytes".format(log_file_size))
        if log_file_size > MAX_LOG_FILE_SIZE:
            with open(LOG_FILE_NAME, 'w'):
                pass
            logging.info("Cleaned log")
