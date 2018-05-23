# options.py
# class for wrapping options for esa_master_downloader script
# Author: Hal DiMarchi

from . import log
from configparser import SafeConfigParser
import json
import os


class Options:
    def __init__(self, downloader_path):
        self.name = "esa_master_downloader"
        self.config_path = os.path.abspath(os.path.join(downloader_path, "config"))
        self.config_file = os.path.join(self.config_path, self.name + '.cfg')

        self.config = SafeConfigParser()
        self.config.read(self.config_file)
        self.get_options()

    def get_options(self):
        self.password = self.config.get('general', 'password')
        self.esa_data_db = self.db_connection_string('esa_data')
        self.get_granule_from_esa_data = self.config.get('sql', 'get_granule')
        self.update_downloaded_for_esa_data = self.config.get('sql', 'download')
        self.max_processes = int(self.config.get('multiprocessing',
                                                 'max_processes'))
        self.wait_period = int(self.config.get('general', 'wait_period'))
        self.run = int(self.config.get('general', 'run'))

        self.usernames = json.loads(self.config.get("users", "usernames"))

        self.get_and_set_running()

    def get_and_set_running(self):
        self.running = int(self.config.get('general', 'running'))
        if self.running:
            raise Exception("Downloader is already running")
        self.set_running('1')

    def set_running(self, running):
        self.config.set('general', 'running', running)
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)

    def update_max_processes_and_run(self):
        log.info("Reading config file")
        log.info("Updating max processes, and run")
        self.config.read(self.config_file)
        self.max_processes = int(self.config.get('multiprocessing',
                                                 'max_processes'))
        self.run = int(self.config.get('general', 'run'))
        log.info("Run is now {}".format(self.run))

    def db_connection_string(self, db):
        connection_string = \
            "host='" + self.config.get(db, 'host') + "' " + \
            "dbname='" + self.config.get(db, 'db') + "' " + \
            "user='" + self.config.get(db, 'user') + "' " + \
            "password='" + self.config.get(db, 'pass') + "'"

        return connection_string
