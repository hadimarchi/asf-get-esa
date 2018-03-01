# esa_master_downloader.py
# script for managing downloading of high priority products
# from ESA
# Author: Hal DiMarchi

import os
from master_utils import master

if __name__ == '__main__':
    master = master.Master(os.path.dirname(__file__))
    master.idle()
