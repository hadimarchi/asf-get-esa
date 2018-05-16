# __init__.py
# Author: Hal DiMarchi
# utils package for esa_watcher script

import logging

logging.basicConfig(filename='watcher.log',
                    level=logging.DEBUG,
                    format='%(filename)s %(funcName)s %(levelname)s: %(message)s')


def get_product_dict(product):
    return {'granule': product[0],
            'url': product[1]}
