# esa_watcher
# Author: Hal DiMarchi
# Grabs high interest SLC products from ESA

import ConfigParser
import logging
from lxml import etree
from optparse import OptionParser
import os
import psycopg2

logging.basicConfig(level=logging.DEBUG,
                    format='%(pathname)s %(asctime)s %(levelname)s %(message)s')
