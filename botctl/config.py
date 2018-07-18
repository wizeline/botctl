import json
import logging
import os

from configparser import ConfigParser


from botctl.errors import (
    UndefinedConfigSection,
    UndefinedConfigValue
)


__configdir__ = os.path.join(os.environ['HOME'], '.botctl')
logger = logging.getLogger(__name__)


class ConfigStore:
    def __init__(self):
        self._config = ConfigParser()
        self._path = os.path.join(__configdir__, 'config.ini')

        if os.path.exists(self._path):
            self._config.read(self._path)
        elif not os.path.exists(__configdir__):
            os.mkdir(__configdir__)

    def del_value(self, variable, section='DEFAULT'):
        try:
            del self._config[section][variable]
        except KeyError as ex:
            missing_key = ex.args[0]
            if missing_key == section:
                raise UndefinedConfigSection(missing_key)
            else:
                raise UndefinedConfigValue(section, missing_key)

    def get_value(self, variable, section='DEFAULT'):
        try:
            return self._config[section][variable]
        except KeyError as ex:
            missing_key = ex.args[0]
            if missing_key == section:
                raise UndefinedConfigSection(missing_key)
            else:
                raise UndefinedConfigValue(section, missing_key)

    def put_value(self, variable, value, section='DEFAULT'):
        try:
            self._config[section].update({variable: value})
        except KeyError:
            raise UndefinedConfigSection(section)

    def add_section(self, section):
        self._config[section] = {}

    def commit(self):
        with open(self._path, 'w') as config_file:
            self._config.write(config_file)
