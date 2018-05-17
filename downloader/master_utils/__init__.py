# __init__.py for
# master_utils module
# Author: Hal DiMarchi

import logging
logging.basicConfig(filename='master.log',
                    level=logging.DEBUG,
                    format='%(filename)s %(funcName)s %(levelname)s: %(message)s')


def get_product_from_url(product):
    url = product[1]
    granule = product[0]
    url = url.replace("https://scihub.copernicus.eu/apihub/odata/v1/Products('", '')
    url = url.replace(")/Products('Quicklook')", '')
    return (granule, url.replace("'/$value", ''))
