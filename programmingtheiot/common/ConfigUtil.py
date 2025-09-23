import configparser
import logging

class ConfigUtil:
    def __init__(self, configFile):
        self.configFile = configFile
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.configFile)
        except Exception as e:
            logging.warning("Could not read config file: %s", e)

    def getBoolean(self, section, key):
        try:
            return self.config.getboolean(section, key)
        except:
            # Default to False if not found
            return False
