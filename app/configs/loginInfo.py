import configparser

config_file = 'configs/config.ini'

class ConfigReader:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_database_config(self):
        db_config = {
            'host': self.config['database']['host'],
            'user': self.config['database']['user'],
            'password': self.config['database']['password'],
            'database': self.config['database']['database'],
            'port' = self.config['database']['port']
        }
        return db_config
