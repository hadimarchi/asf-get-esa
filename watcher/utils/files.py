# files.py
# Author: Hal DiMarchi
# File path setup for watcher

from bs4 import BeautifulSoup
import os


class Files():
    def __init__(self, watcher_path, log):
        self.name = 'esa_watcher'
        self.watcher_path = watcher_path
        self.log = log
        self.config_path = os.path.abspath(os.path.join(self.watcher_path, "config"))
        self.config = os.path.join(self.config_path, self.name + '.cfg')
        self.last_file = os.path.join(self.config_path, 'last_granule.txt')
        self.xml_path = os.path.abspath(os.path.join(self.watcher_path, "xml"))
        self.base_xml = os.path.join(self.xml_path, 'xml_filelist_' + str(os.getpid()))

    def parse_esa_xml(self):
        with open(self.target_xml) as xml_file:
            xml = BeautifulSoup(xml_file, "lxml")

        products = []
        for product in xml.find_all('entry'):
            id = product.find("id").string
            title = product.find("title").string

            data_type = title[7:10]
            if "SLC" not in data_type:
                self.log.info("NON SLC PRODUCT: {}\nIGNORING".format(title))
                continue

            footprint = product.find(attrs={"name": "footprint"}).string
            products.append(dict(id=id, title=title, data_type=data_type, footprint=footprint))

        return products
