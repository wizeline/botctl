import logging
import os
import subprocess
import sys

from botctl.config import ConfigStore
from botctl.errors import BotControlError
from botctl.types import PlatformEnvironment, PlatformVariable


logger = logging.getLogger(__name__)


def command_callback(callback):
    def callback_wrapper(*args, **kwargs):
        try:
            rc = callback(*args, **kwargs)

        except BotControlError as expected_error:
            logger.debug(expected_error)
            sys.stderr.write(f'{expected_error}\n')
            rc = -1

        return rc

    return callback_wrapper


def parse_variable(config, raw_variable):
    if '/' in raw_variable:
        prefix, str_variable = raw_variable.split('/')
        environment = PlatformEnvironment(prefix.upper())
        variable = PlatformVariable(str_variable)
    else:
        environment = config.get_environment()
        variable = PlatformVariable(raw_variable)

    return environment, variable


def display_help(command):
    if command is None:
        sys.stderr.write('Unknown command\n')
        return 1

    print(command.help())
    return 0


def display_manual(command_name):
    man_page = os.path.join(os.environ['HOME'],
                            '.botctl',
                            'man',
                            '1',
                            f'{command_name}.1')
    subprocess.call(['man', man_page])


def execute_subcommand(command_name, **callbacks):
    if len(sys.argv) == 1:
        display_manual(command_name)
        return -1

    subcommand, args = sys.argv[1], sys.argv[2:]

    if subcommand == 'help':
        display_manual(command_name)
        return 0

    action_klass = callbacks.get(command_name)
    if not action_klass:
        display_manual(command_name)
        return 1

    action = action_klass(ConfigStore())
    rc = action(*args)
    if rc != 0:
        action.help()

    return rc
