import logging
import sys

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
