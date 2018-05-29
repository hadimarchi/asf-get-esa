from configparser import SafeConfigParser


class Base_Options:
    def __init__(self):
        pass

    def get_config(self):
        self.config = SafeConfigParser()
        self.config.read(self.config_file)

    def db_connection_string(self, db):
        connection_string = \
            "host='" + self.config.get(db, 'host') + "' " + \
            "dbname='" + self.config.get(db, 'db') + "' " + \
            "user='" + self.config.get(db, 'user') + "' " + \
            "password='" + self.config.get(db, 'pass') + "'"

        return connection_string


class Main_Options(Base_Options):
    def get_and_set_running(self):
        self.get_running()
        self.set_running('1')

    def get_running(self):
        self.running = int(self.config.get('general', 'running'))
        if self.running:
            raise Exception()

    def set_running(self, running):
        self.config.set('general', 'running', running)
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)
