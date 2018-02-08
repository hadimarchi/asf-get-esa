# master.py
# master of child processes in children class
# Author: Hal DiMarchi

from multiprocessing import Pool, Process
from .children import Children
from .sql import Esa_Data_Sql


class Master:
    def __init__(self):
        self.children = Children()

    def get_products(self):
        pass
