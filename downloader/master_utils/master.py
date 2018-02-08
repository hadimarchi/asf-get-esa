# master.py
# master of child processes in children class
# Author: Hal DiMarchi

from multiprocessing import Pool, Process
from .children import Children
from utils.error import DownloadError
from .sql import Esa_Data_Sql
from .options import Options


class Master:
    def __init__(self, location):
        self.children = Children()
        self.options = Options(location)
        self.sql = Esa_Data_Sql(self.options)

    def get_products_from_db(self):
        self.products = self.sql.get_granules()
