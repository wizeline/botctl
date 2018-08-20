import sys

from botctl.common import command_callback, display_help, parse_variable
from botctl.config import ConfigStore
from botctl.types import PlatformEnvironment, BotControlCommand


class DelCommand(BotControlCommand):
    """Usage:
    $ botctl del <variable>
    """
    __commandname__ = 'del'

    @command_callback
    def __call__(self, variable_name):
        environment, variable = parse_variable(self.config, variable_name)
        self.config.del_value(environment, variable)
        self.config.commit()


class GetCommand(BotControlCommand):
    """Usage:
    $ botctl get <variable>
    """
    __commandname__ = 'get'

    @command_callback
    def __call__(self, variable_name):
        environment, variable = parse_variable(self.config, variable_name)
        print(self.config.get_value(environment, variable))


class SetCommand(BotControlCommand):
    """Usage
    $ botctl set <variable> <value>
    """
    __commandname__ = 'set'

    @command_callback
    def __call__(self, variable_name, variable_value):
        environment, variable = parse_variable(self.config, variable_name)
        self.config.put_value(environment, variable, variable_value)
        self.config.commit()


class ChangeEnvironmentCommand(BotControlCommand):
    """Usage
    $ botctl chenv {local | development | production}
    """
    __commandname__ = 'chenv'

    @command_callback
    def __call__(self, environment_name):
        environment = PlatformEnvironment(environment_name.upper())
        self.config.set_environment(environment)
        self.config.commit()


def main():
    config = ConfigStore()
    command = sys.argv[1]
    args = sys.argv[2:]

    callbacks = {
        'set': SetCommand(config),
        'get': GetCommand(config),
        'del': DelCommand(config),
        'chenv': ChangeEnvironmentCommand(config)
    }

    if command == 'help':
        action = callbacks.get(args[0])
        sys.exit(display_help(callbacks.get(args[0])))

    else:
        action = callbacks.get(command)
        if action is None:
            sys.stderr.write('Unknown command\n')
            sys.exit(2)
        sys.exit(action(*args))
