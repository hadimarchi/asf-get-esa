# sql.py
# class for connecting with esa_data
# Author: Hal DiMarchi

try:
    import psycopg2
except ImportError:
    import psycopg2cffi as psycopg2


class Esa_Data_Sql:
    def __init__(self):
        pass
