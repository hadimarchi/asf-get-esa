# options.py
# Author: Hal DiMarchi
# sets up options for downloader

from configparser import SafeConfigParser
import os


class Options():
    def __init__(self, downloader_path, username):
        self.name = "esa_child_downloader"
        self.config_path = os.path.abspath(os.path.join(downloader_path, "config"))
        self.config_file = os.path.join(self.config_path, self.name + '.cfg')

        self.config = SafeConfigParser()
        self.config.read(self.config_file)
        self.user = username
        self.get_options()

    def get_options(self):
        self.password = self.config.get('general', 'password')
        self.esa_host = self.config.get('general', 'ESA_host')
        self.download_dir = self.config.get('general', 'download_dir')
        self.final_dir = os.path.abspath(self.config.get('general', 'final_dir'))

        self.pg_db = self.db_connection_string('pg_db_sql')
        self.find_granule_sql = self.config.get('pg_db_sql', 'find_granule_sql')

    def db_connection_string(self, db):
        connection_string = \
            "host='" + self.config.get(db, 'host') + "' " + \
            "dbname='" + self.config.get(db, 'db') + "' " + \
            "user='" + self.config.get(db, 'user') + "' " + \
            "password='" + self.config.get(db, 'pass') + "'"

        return connection_string
