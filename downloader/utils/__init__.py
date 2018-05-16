# __init__.py
# Author: Hal DiMarchi
# utils package for esa_downloader script

import logging

logging.basicConfig(filename='master.log',
                    level=logging.DEBUG,
                    format='%(filename)s %(funcName)s %(levelname)s: %(message)s')
