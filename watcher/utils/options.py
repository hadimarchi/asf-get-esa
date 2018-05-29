# options.py
# Author: Hal DiMarchi
# sets up options for watcher

import json
import os
from datetime import datetime

from importlib.machinery import SourceFileLoader as load
options = load("share.options", "../shared/options.py").load_module()


class Options(options.Main_Options):
    def __init__(self, watcher_path):
        self.name = "esa_watcher"
        self.config_path = os.path.abspath(os.path.join(watcher_path, "config"))
        self.config_file = os.path.join(self.config_path, self.name + '.cfg')

        super().get_config()
        self.get_options()

    def get_options(self):
        self.user = self.config.get('general', 'username')
        self.password = self.config.get('general', 'password')
        self.num_back = int(self.config.get('fetch', 'num_back'))
        self.last_search_time = (self.config.get('fetch', 'last_search_time',
                                 fallback=datetime.isoformat(datetime.now())))
        self.users = ','.join(str(user) for user in json.loads(self.config.get('general', 'users')))
        self.hyp3_db = self.db_connection_string("hyp3-db")
        self.pg_db = self.db_connection_string("pgsql")
        self.esa_data_db = self.db_connection_string("esa_data")

        self.find_granules_in_pg_sql = self.config.get('sql', 'pg_db_sql')
        self.intersects_hyp3_subs_sql = self.config.get('sql', 'intersects_subs_sql')
        self.insert_sql = self.config.get('sql', 'insert_sql')

        try:
            self.get_and_set_running()
        except Exception as e:
            raise Exception("Watcher is already running")

    def update_last_search_time(self):
        self.config.set('fetch', 'last_search_time', datetime.isoformat(datetime.now()))
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)
