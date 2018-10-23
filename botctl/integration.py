import json
import re
import sys

from json.decoder import JSONDecodeError

from botctl.client import IntegrationClientCommand
from botctl.common import command_callback, execute_subcommand


class CallIntegrationCommand(IntegrationClientCommand):
    """Usage:
    $ callint {INTEGRATION_NAME}.{FUNCTION_NAME} [ARGS,...]
    """
    __commandname__ = 'integration call'

    @command_callback
    def __call__(self, function_spec):
        integration, function = function_spec.split('.')
        payload = self._build_function_payload(integration, function)

        result = self.client.call_function(
            integration,
            function,
            payload
        )
        print(json.dumps(result, indent=2))
        return 0

    def _build_function_payload(self, integration, function):
        return {
            'parameters': json.load(sys.stdin),
            'configuration': self.config.get_integration_config(integration),
            'credentials': ''
        }


class ConfigureIntegrationCommand(IntegrationClientCommand):
    """Usage:
    $ integration config {INTEGRATION_NAME} < INTEGRATION_CONFIG.json
    """

    __commandname__ = 'integration config'

    @command_callback
    def __call__(self, integration_name):
        integration_config = sys.stdin.read()
        try:
            rc = self._store_integration_config(integration_name,
                                                integration_config)
        except JSONDecodeError:
            sys.stderr.write('Integration config must be a JSON document\n')
            return 1
        return rc

    def _store_integration_config(self, integration_name, integration_config):
        integration = self.client.get_integration(
            integration_name
        )
        parsed_config = json.loads(integration_config)
        expected_options = integration['configuration_options'].keys()
        options = parsed_config.keys()

        if expected_options != options:
            sys.stdout.write('Configuration mismatch\n\n')
            self._dump_config_options(integration)
            return 1
        self.config.set_integration_config(
            integration_name,
            json.dumps(parsed_config)
        )
        self.config.commit()


class IntegrationLister(IntegrationClientCommand):
    """Usage:
    $ integration list
    """

    __commandname__ = 'integration list'

    @command_callback
    def __call__(self, *args):  # Include args to meet the command interface
        for integration_name in self.client.get_integrations():
            print(integration_name)


class ShowIntegrationCommand(IntegrationClientCommand):
    """Usage:
    $ integration show {INTEGRATION_NAME}[.{FUNCTION_NAME}]
    """
    __commandname__ = 'integration show'

    @command_callback
    def __call__(self, function_spec):
        integration_name, function_name = self._parse_function_spec(
            function_spec
        )
        if function_name:
            rc = self.show_function(integration_name, function_name)
        else:
            rc = self.show_integration(integration_name)

        return rc

    def _parse_function_spec(self, spec):
        match = re.match('(\w+)(\.\w+)?', spec)
        assert match, f'Not a valid integration or function: {spec}'
        integration, function = match.groups()

        if function:
            # Removethe leading dot at `function`
            return integration, function[1:]
        else:
            return integration, function

    def show_function(self, integration_name, function_name):
        function_spec = self.client.get_function(integration_name, function_name)
        self.dump_function(integration_name, function_name, function_spec)
        return 0

    def show_integration(self, integration_name):
        integration = self.client.get_integration(integration_name)
        self.dump_integration(integration)
        return 0


def main():
    callbacks = {
        'call': CallIntegrationCommand,
        'config': ConfigureIntegrationCommand,
        'list': IntegrationLister,
        'show': ShowIntegrationCommand
    }
    return execute_subcommand('integration', **callbacks)
