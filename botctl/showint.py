import sys

from botctl.client import IntegrationClientCommand
from botctl.common import command_callback
from botctl.config import ConfigStore


class ShowIntegrationCommand(IntegrationClientCommand):
    """Usage:
    $ showint {INTEGRATION_NAME}[.{FUNCTION_NAME}]
    """
    __commandname__ = 'showint'

    @command_callback
    def __call__(self, integration_name, function_name=''):
        integration = self.client.get_integration(integration_name)
        if integration:
            self.dump_integration(integration)
            return 0
        else:
            sys.stderr.write(f'Integration not found: {integration_name}\n')
            return 1


def main():
    command = ShowIntegrationCommand(ConfigStore())
    if len(sys.argv) != 2:
        print(command.help())
        sys.exit(1)

    integration_name = sys.argv[1]
    sys.exit(command(integration_name))
