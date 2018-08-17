import sys

from botctl.common import command_callback, parse_variable
from botctl.config import ConfigStore
from botctl.types import PlatformEnvironment


@command_callback
def del_config_value(config, variable_name):
    environment, variable = parse_variable(config, variable_name)
    config.del_value(environment, variable)
    config.commit()


@command_callback
def get_config_value(config, variable_name):
    environment, variable = parse_variable(config, variable_name)
    print(environment, variable)
    print(config.get_value(environment, variable))


@command_callback
def set_config_value(config, variable_name, variable_value):
    environment, variable = parse_variable(config, variable_name)
    config.put_value(environment, variable, variable_value)
    config.commit()


@command_callback
def change_environment(config, environment_name):
    environment = PlatformEnvironment(environment_name.upper())
    config.set_environment(environment)
    config.commit()


def main():
    config = ConfigStore()
    command = sys.argv[1]
    args = sys.argv[2:]

    callbacks = {
        'set': set_config_value,
        'get': get_config_value,
        'del': del_config_value,
        'chenv': change_environment
    }

    action = callbacks[command]
    sys.exit(action(config, *args))
