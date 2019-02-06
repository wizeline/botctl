import json
import logging
import os
import re

from configparser import RawConfigParser

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
        self._config = RawConfigParser()
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

    def _get_integration_config_slot(self, integration_name):
        environment = self.get_environment()
        return f'{environment.value}/integrations/{integration_name}'

    def _get_integration_credentials_slot(self, integration_name):
        environment = self.get_environment()
        return f'{environment.value}/integrations/{integration_name}/credentials'

    def _parse_value(self, value):
        try:
            return int(value)
        except:
            return value

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

    def get_integration_config(self, integration_name):
        integration_slot = self._get_integration_slot(integration_name)

        return {
            option: self._parse_value(value)
            for option, value in self._config[integration_slot].items()
        }

    def get_value(self, environment, variable):
        if not self.has_environment(environment):
            raise UndefinedConfigSection(environment.value)

        values = self._config[environment.value]

        if variable.value not in values:
            raise UndefinedConfigValue(environment, variable)

        return self._config[environment.value][variable.value]

    def has_environment(self, environment):
        return self._config.has_section(environment.value)

    def put_value(self, environment, variable, value):
        try:
            self._config[environment.value].update({variable.value: value})
        except KeyError:
            raise UndefinedConfigSection(environment)

    def set_environment(self, environment):
        self._config[SYSTEM_SECTION]['environment'] = environment.value

    def set_integration_config(self, integration_name, integration_config):
        integration_slot = self._get_integration_slot(integration_name)

        if not self._config.has_section(integration_slot):
            self._config.add_section(integration_slot)

        for option, value in integration_config.items():
            try:
                self._config[integration_slot][option] = str(value)
            except TypeError as error:
                print(f'Error: {type(error)}: {error}')
                print(f'{integration_slot} {option} {value}')
                raise error
