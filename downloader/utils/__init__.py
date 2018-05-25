# __init__.py
# Author: Hal DiMarchi
# utils package for esa_downloader script

import logging
import os

logging.basicConfig(filename='master.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s')


def ensure_paths(paths):
    for path in paths:
        ensure_path(path)


def ensure_path(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path)
