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
        self.download_dir = self.config.get('general', 'download_dir')

    def get_authenticated_url(self, url):
        authenticated_url = "https://{}:{}@{}".format(
                                                      self.user,
                                                      self.password,
                                                      url
                                                      )
        print(authenticated_url)
        return authenticated_url
