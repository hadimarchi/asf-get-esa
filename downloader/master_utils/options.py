# options.py
# class for wrapping options for esa_master_downloader script
# Author: Hal DiMarchi

from . import log
import json
import os

from importlib.machinery import SourceFileLoader as load
options = load("share.options", "../shared/options.py").load_module()


class Options(options.Main_Options):
    def __init__(self, downloader_path):
        self.name = "esa_master_downloader"
        self.config_path = os.path.abspath(os.path.join(downloader_path, "config"))
        self.config_file = os.path.join(self.config_path, self.name + '.cfg')

        super().get_config()
        self.get_options()

    def get_options(self):
        self.esa_data_db = self.db_connection_string('esa_data')
        self.get_granule_from_esa_data = self.config.get('sql', 'get_granule')
        self.update_downloaded_for_esa_data = self.config.get('sql', 'download')
        self.max_processes = int(self.config.get('multiprocessing',
                                                 'max_processes'))
        self.wait_period = int(self.config.get('general', 'wait_period'))
        self.run = int(self.config.get('general', 'run'))

        self.usernames = json.loads(self.config.get("users", "usernames"))

        try:
            self.get_and_set_running()
        except Exception:
            raise Exception("Downloader is already running")

    def update_max_processes_and_run(self):
        log.info("Reading config file")
        log.info("Updating max processes, and run")
        self.config.read(self.config_file)
        self.max_processes = int(self.config.get('multiprocessing',
                                                 'max_processes'))
        self.run = int(self.config.get('general', 'run'))
        log.info("Run is now {}".format(self.run))
