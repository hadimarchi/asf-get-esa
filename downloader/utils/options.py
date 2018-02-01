# options.py
# Author: Hal DiMarchi
# sets up options for downloader

from configparser import SafeConfigParser


class Options():
    def __init__(self, config_file):
        self.config = SafeConfigParser()
        self.config.read(config_file)
        self.get_options()

    def get_options(self):
        self.user = self.options.user = self.config.get('general', 'username')
        self.password = self.config.get('general', 'password')
        self.esa_host = self.config.get('general', 'ESA_host')
        self.esa_data_db = self.db_connection_string('esa_data')
        self.get_granule_from_esa_data = self.config.get('sql', 'get_granule')

    def db_connection_string(self, db):
        connection_string = \
            "host='" + self.config.get(db, 'host') + "' " + \
            "dbname='" + self.config.get(db, 'db') + "' " + \
            "user='" + self.config.get(db, 'user') + "' " + \
            "password='" + self.config.get(db, 'pass') + "'"

        return connection_string

    def esa_query_url(self, url):
        authenticated_url = "https://{}:{}@{}".format(
                                                      self.user,
                                                      self.options,
                                                      url
                                                      )
        return authenticated_url
