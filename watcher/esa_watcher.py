# esa_watcher
# Author: Hal DiMarchi
# Grabs high interest SLC products from ESA

import os
from utils import watcher, logging as log


if __name__ == "__main__":
    log.info("Spinning up")
    watcher = watcher.Watcher(os.path.dirname(__file__))
    watcher.find_candidate_products()
    watcher.filter_for_unknown_products()
    watcher.filter_for_subscription_intersection()
    watcher.insert_products_in_db()
    log.info("Done")
