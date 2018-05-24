# options.py
# Author: Hal DiMarchi
# sets up options for watcher

import json
import os
from datetime import datetime
from configparser import SafeConfigParser


class Options:
    def __init__(self, watcher_path):
        self.name = "esa_watcher"
        self.config_path = os.path.abspath(os.path.join(watcher_path, "config"))
        self.config_file = os.path.join(self.config_path, self.name + '.cfg')
        self.config = SafeConfigParser()
        self.config.read(self.config_file)
        self.get_options()

    def get_options(self):
        self.user = self.config.get('general', 'username')
        self.password = self.config.get('general', 'password')
        self.num_back = int(self.config.get('fetch', 'num_back'))
        self.last_search_time = (self.config.get('fetch', 'last_search_time',
                                 fallback=datetime.isoformat(datetime.min)))
        self.users = ','.join(str(user) for user in json.loads(self.config.get('general', 'users')))
        self.hyp3_db = self.db_connection_string("hyp3-db")
        self.pg_db = self.db_connection_string("pgsql")
        self.esa_data_db = self.db_connection_string("esa_data")

        self.find_granules_in_pg_sql = self.config.get('sql', 'pg_db_sql')
        self.intersects_hyp3_subs_sql = self.config.get('sql', 'intersects_subs_sql')
        self.insert_sql = self.config.get('sql', 'insert_sql')

        self.get_and_set_running()

    def get_and_set_running(self):
        self.get_running()
        self.set_running('1')

    def get_running(self):
        self.running = int(self.config.get('general', 'running'))
        if self.running:
            raise Exception("Watcher is already running")

    def set_running(self, running):
        self.config.set('general', 'running', running)
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)

    def db_connection_string(self, db):
        connection_string = \
            "host='" + self.config.get(db, 'host') + "' " + \
            "dbname='" + self.config.get(db, 'db') + "' " + \
            "user='" + self.config.get(db, 'user') + "' " + \
            "password='" + self.config.get(db, 'pass') + "'"

        return connection_string

    def update_last_search_time(self):
        self.config.set('fetch', 'last_search_time', datetime.isoformat(datetime.now()))
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)
