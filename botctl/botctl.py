import sys

from botctl.common import command_callback
from botctl.config import ConfigStore


@command_callback
def del_config_value(config, variable_name):
    config.del_value(variable_name)
    config.commit()


@command_callback
def get_config_value(config, variable_name):
    print(config.get_value(variable_name))


@command_callback
def set_config_value(config, variable_name, variable_value):
    config.put_value(variable_name, variable_value)
    config.commit()


def main():
    config = ConfigStore()
    command = sys.argv[1]
    args = sys.argv[2:]

    callbacks = {
        'set': set_config_value,
        'get': get_config_value,
        'del': del_config_value
    }

    action = callbacks[command]
    sys.exit(action(config, *args))
