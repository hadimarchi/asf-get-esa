# options.py
# Author: Hal DiMarchi
# sets up options for downloader

from configparser import SafeConfigParser
import os


class Options():
    def __init__(self, downloader_path):
        self.name = "esa_downloader"
        self.config_path = os.path.abspath(os.path.join(downloader_path, "config"))
        self.config_file = os.path.join(self.config_path, self.name + '.cfg')

        self.config = SafeConfigParser()
        self.config.read(self.config_file)
        self.get_options()

    def get_options(self):
        self.user = self.config.get('general', 'username')
        self.password = self.config.get('general', 'password')
        self.esa_host = self.config.get('general', 'ESA_host')
        self.esa_data_db = self.db_connection_string('esa_data')
        self.get_granule_from_esa_data = self.config.get('sql', 'get_granule')
        self.update_downloaded_for_esa_data = self.config.get('sql', 'download')
        self.download_dir = self.config.get('general', 'download_dir')

    def db_connection_string(self, db):
        connection_string = \
            "host='" + self.config.get(db, 'host') + "' " + \
            "dbname='" + self.config.get(db, 'db') + "' " + \
            "user='" + self.config.get(db, 'user') + "' " + \
            "password='" + self.config.get(db, 'pass') + "'"

        return connection_string

    def get_authenticated_url(self, url):
        authenticated_url = "https://{}:{}@{}".format(
                                                      self.user,
                                                      self.password,
                                                      url
                                                      )
        print(authenticated_url)
        return authenticated_url
