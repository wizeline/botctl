import logging
import os

from configparser import RawConfigParser

from botctl.errors import (
    UndefinedConfigSection,
    UndefinedConfigValue
)
from botctl.types import PlatformEnvironment, PlatformVariable


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

        self._load()

        for env in PlatformEnvironment.values():
            if not self.has_environment(env):
                self.add_environment(env)

    def _load(self):
        if not self._config.has_section(SYSTEM_SECTION):
            self._config[SYSTEM_SECTION] = {}
            self.set_environment(PlatformEnvironment.LOCAL)

    def _get_integration_config_slot(self, integration_name):
        environment = self.get_environment()
        return f'{environment.value}/integrations/{integration_name}/config'

    def _get_integration_credentials_slot(self, integration_name):
        environment = self.get_environment()
        return (f'{environment.value}/integrations/'
                f'{integration_name}/credentials')

    def _parse_value(self, value):
        try:
            return int(value)
        except Exception:
            return value

    def _setup_environment(self, environment, values):
        if not self.has_environment(environment):
            self.add_environment(environment)

        for variable, value in values.items():
            self.put_value(environment, variable, value)

    def _setup_local(self):
        values = {
            PlatformVariable.FRONTEND: 'http://localhost:8000',
            PlatformVariable.CMS: 'http://localhost:8001',
            PlatformVariable.INTEGRATIONS_MANAGER: 'http://localhost:8002',
            PlatformVariable.OPERATIONS: 'http://localhost:8003',
        }
        self._setup_environment(PlatformEnvironment.LOCAL, values)

    def _setup_development(self):
        values = {
            PlatformVariable.FRONTEND: (
                'https://cms-frontend-development.bots-platform.com'
            ),
            PlatformVariable.CMS: (
                'https://cms-backend-development.bots-platform.com'
            ),
            PlatformVariable.INTEGRATIONS_MANAGER: (
                'https://integrations-manager-development.bots-platform.com'
            ),
            PlatformVariable.OPERATIONS: (
                'https://operations-controller-development.bots-platform.com'
            )
        }
        self._setup_environment(PlatformEnvironment.DEVELOPMENT, values)

    def _setup_staging(self):
        values = {
            PlatformVariable.FRONTEND: (
                'https://cms-frontend-staging.bots-platform.com'
            ),
            PlatformVariable.CMS: (
                'https://cms-backend-staging.bots-platform.com'
            ),
            PlatformVariable.INTEGRATIONS_MANAGER: (
                'https://integrations-manager-staging.bots-platform.com'
            ),
            PlatformVariable.OPERATIONS: (
                'https://operations-controller-staging-lb.bots-platform.com'
            )
        }

        self._setup_environment(PlatformEnvironment.STAGING, values)

    def _setup_performance(self):
        values = {
            PlatformVariable.FRONTEND: ( # CMS frontend will be the same AFAIK
                'https://cms-frontend-development.bots-platform.com'
            ),
            PlatformVariable.CMS: (  # CMS backend is coming soon
                'https://cms-backend-development.bots-platform.com'
            ),
            PlatformVariable.INTEGRATIONS_MANAGER: (
                'https://integrations-manager-performance.bots-platform.com'
            ),
            PlatformVariable.OPERATIONS: (
                'https://operations-controller-performance.bots-platform.com'
            )
        }
        self._setup_environment(PlatformEnvironment.PERFORMANCE, values)

    def _setup_production(self):
        values = {
            PlatformVariable.FRONTEND: 'https://bots.wizeline.com',
            PlatformVariable.CMS: (
                'https://cms-backend-production.bots-platform.com'
            ),
            PlatformVariable.INTEGRATIONS_MANAGER: (
                'https://integrations-manager-production-lb.bots-platform.com'
            ),
            PlatformVariable.OPERATIONS: (
                'https://bots-api.wizeline.com'
            )
        }

        self._setup_environment(PlatformEnvironment.PRODUCTION, values)

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
        integration_slot = self._get_integration_config_slot(integration_name)

        if not self.has_section(integration_slot):
            return {}

        return self.get_values_from_section(integration_slot)

    def get_integration_credentials(self, integration_name):
        integration_slot = self._get_integration_credentials_slot(
            integration_name
        )

        if not self.has_section(integration_slot):
            return {}

        return self.get_values_from_section(integration_slot)

    def get_value(self, environment, variable):
        if not self.has_environment(environment):
            raise UndefinedConfigSection(environment.value)

        values = self._config[environment.value]

        if variable.value not in values:
            raise UndefinedConfigValue(environment, variable)

        return self._config[environment.value][variable.value]

    def get_values_from_section(self, section):
        return {
            option: self._parse_value(value)
            for option, value in self._config[section].items()
        }

    def has_environment(self, environment):
        return self.has_section(environment.value)

    def has_section(self, section):
        return self._config.has_section(section)

    def put_value(self, environment, variable, value):
        try:
            self._config[environment.value].update({variable.value: value})
        except KeyError:
            raise UndefinedConfigSection(environment)

    def set_environment(self, environment):
        self._config[SYSTEM_SECTION]['environment'] = environment.value

    def set_integration_config(self, integration_name, integration_config):
        integration_slot = self._get_integration_config_slot(integration_name)

        if not self._config.has_section(integration_slot):
            self._config.add_section(integration_slot)

        self.set_values_at_section(integration_slot, **integration_config)

    def set_integration_credentials(self,
                                    integration_name,
                                    integration_credentials):
        integration_slot = self._get_integration_credentials_slot(
            integration_name
        )

        if not self._config.has_section(integration_slot):
            self._config.add_section(integration_slot)

        self.set_values_at_section(integration_slot, **integration_credentials)

    def set_values_at_section(self, section, **kwvalues):
        for option, value in kwvalues.items():
            self._config[section][option] = str(value)

    def setup(self):
        self._setup_local()
        self._setup_development()
        self._setup_staging()
        self._setup_performance()
        self._setup_production()
