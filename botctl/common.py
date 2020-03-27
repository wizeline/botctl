import json
import logging
import os
import re
import subprocess
import sys

from botctl import errors
from botctl.config import ConfigStore
from botctl.types import PlatformEnvironment, PlatformVariable


logger = logging.getLogger(__name__)


def is_usage_error(error):
    matches = re.match(
        '__call__\(\) missing .* required positional argument',  # noqa
        str(error)
    )

    return matches is not None


def parse_input(stream=sys.stdin):
    input_buffer = stream.read()
    try:
        return json.loads(input_buffer)
    except json.decoder.JSONDecodeError:
        pass  # The content might be in YAML format
    except Exception as error:
        raise errors.BotControlError(
            f'Unexpected error reading input JSON stream: {error}'
        )

    try:
        return yaml.load(input_buffer)
    except Exception as error:
        raise errors.BotControlError(
            f'Unexpected error reading input YAML stream: {error}'
        )


def command_callback(callback):
    def callback_wrapper(this, *args, **kwargs):
        if this.expects_input:
            setattr(this, 'input', parse_input())

        try:
            rc = callback(this, *args, **kwargs)

        except errors.BotControlError as expected_error:
            sys.stderr.write(f'{expected_error}\n')
            rc = -1

        except TypeError as error:

            if is_usage_error(error):
                display_help(this)
                rc = -2
            else:
                raise error

        return rc

    return callback_wrapper


def parse_variable(config, raw_variable):
    if '/' in raw_variable:
        tokens = raw_variable.split('/')

        if len(tokens) != 2:
            raise errors.InvalidVariableName(raw_variable)

        prefix, str_variable = tokens
        environment_name = prefix.upper()

        if not PlatformEnvironment.is_valid(environment_name):
            raise errors.InvalidPlatformEnvironment(prefix)

        if not PlatformVariable.is_valid(str_variable):
            raise errors.InvalidVariableName(str_variable)

        environment = PlatformEnvironment(environment_name)

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

    action_klass = callbacks.get(subcommand)
    if not action_klass:
        print(callbacks)
        display_manual(command_name)
        return 1

    action = action_klass(ConfigStore())
    rc = action(*args)
    if rc != 0:
        action.help()

    return rc
