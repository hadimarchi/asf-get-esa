# options.py
# Author: Hal DiMarchi
# sets up options for watcher

import json
from optparse import OptionParser
from configparser import SafeConfigParser


class Config_and_Options():
    def __init__(self, config_file):
        self.config = SafeConfigParser()
        self.config.read(config_file)
        parser = OptionParser()
        parser.add_option(
            "-u", "--user", action="store", dest="user", help="Account name for the ESA data hub"
        )
        parser.add_option(
            "-p", "--password", action="store", dest="password", help="Password for the ESA data hub account"
        )
        parser.add_option(
            "-n", "--num-back", action="store", type="int", dest="num_back", help="How many to check at ESA"
        )
        (self.options, args) = parser.parse_args()

        self.get_options()

    def get_options(self):
        if self.options.user is None:
            self.options.user = self.config.get('general', 'username')
        if self.options.password is None:
            self.options.password = self.config.get('general', 'password')

        if self.options.num_back is None:
            if self.config.has_option('fetch', 'num_back'):
                self.options.num_back = int(self.config.get('fetch', 'num_back'))
            else:
                self.options.num_back = 100
        self.options.inc = int(self.config.get('fetch', 'group_size'))
        self.options.users = ','.join(str(user) for user in json.loads(self.config.get('general', 'users')))
        self.options.hyp3_db = self.db_connection_string("hyp3-db")
        self.options.pg_db = self.db_connection_string("pgsql")
        self.options.esa_data_db = self.db_connection_string("esa_data")

        self.options.find_granules_in_pg_sql = self.config.get('sql', 'pg_db_sql')
        self.options.intersects_hyp3_subs_sql = self.config.get('sql', 'intersects_subs_sql')
        self.options.insert_sql = self.config.get('sql', 'insert_sql')

    def db_connection_string(self, db):
        connection_string = \
            "host='" + self.config.get(db, 'host') + "' " + \
            "dbname='" + self.config.get(db, 'db') + "' " + \
            "user='" + self.config.get(db, 'user') + "' " + \
            "password='" + self.config.get(db, 'pass') + "'"

        return connection_string
