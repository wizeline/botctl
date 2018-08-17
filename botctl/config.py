import logging
import os

from configparser import ConfigParser

from botctl.errors import (
    UndefinedConfigSection,
    UndefinedConfigValue
)
from botctl.types import PlatformEnvironment


__configdir__ = os.path.join(os.environ['HOME'], '.botctl')
logger = logging.getLogger(__name__)
SYSTEM_SECTION = '_SYSTEM'


class ConfigStore:
    def __init__(self):
        self._config = ConfigParser()
        self._path = os.path.join(__configdir__, 'config.ini')

        if os.path.exists(self._path):
            self._config.read(self._path)
        elif not os.path.exists(__configdir__):
            os.mkdir(__configdir__)

        self._setup()

        for env in PlatformEnvironment.values():
            if not self.has_environment(env):
                self.add_environment(env)

    def _setup(self):
        if not self._config.has_section(SYSTEM_SECTION):
            self._config[SYSTEM_SECTION] = {}
            self.set_environment(PlatformEnvironment.LOCAL)

    def add_environment(self, environment):
        self._config[environment.value] = {}

    def commit(self):
        with open(self._path, 'w') as config_file:
            self._config.write(config_file)

    def del_value(self, environment, variable):
        try:
            del self._config[environment.value][variable.value]
        except KeyError as ex:
            missing_key = ex.args[0]
            if missing_key == environment.value:
                raise UndefinedConfigSection(missing_key)
            else:
                raise UndefinedConfigValue(environment.value, missing_key)

    def get_environment(self):
        raw_environment = self._config[SYSTEM_SECTION]['environment']
        return PlatformEnvironment(raw_environment)

    def get_value(self, environment, variable):
        try:
            return self._config[environment.value][variable.value]
        except KeyError as ex:
            missing_key = ex.args[0]
            if missing_key == environment.value:
                raise UndefinedConfigSection(missing_key)
            else:
                raise UndefinedConfigValue(environment, missing_key)

    def has_environment(self, environment):
        return self._config.has_section(environment.value)

    def put_value(self, environment, variable, value):
        try:
            self._config[environment.value].update({variable.value: value})
        except KeyError:
            raise UndefinedConfigSection(environment)

    def set_environment(self, environment):
        self._config[SYSTEM_SECTION]['environment'] = environment.value

