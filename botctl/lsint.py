
import sys

from botctl.client import IntegrationClientCommand
from botctl.common import command_callback
from botctl.config import ConfigStore


class IntegrationLister(IntegrationClientCommand):
    """Usage:
    $ lsint
    """

    __commandname__ = 'lsint'

    @command_callback
    def __call__(self):
        for integration_name in self.client.get_integrations():
            print(integration_name)


def main():
    command = IntegrationLister(ConfigStore())

    if len(sys.argv) > 1:
        print(command.help())
        sys.exit(1)

    sys.exit(command())
