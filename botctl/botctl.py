from botctl.common import command_callback, execute_subcommand, parse_variable
from botctl.types import PlatformEnvironment, BotControlCommand


class DelCommand(BotControlCommand):
    """Usage:
    $ botctl del <variable>
    """
    __commandname__ = 'botctl'

    @command_callback
    def __call__(self, variable_name):
        environment, variable = parse_variable(self.config, variable_name)
        self.config.del_value(environment, variable)
        self.config.commit()
        return 0


class GetCommand(BotControlCommand):
    """Usage:
    $ botctl get <variable>
    """
    __commandname__ = 'botctl'

    @command_callback
    def __call__(self, variable_name):
        environment, variable = parse_variable(self.config, variable_name)
        print(self.config.get_value(environment, variable))
        return 0


class SetCommand(BotControlCommand):
    """Usage
    $ botctl set <variable> <value>
    """
    __commandname__ = 'botctl'

    @command_callback
    def __call__(self, variable_name, variable_value):
        environment, variable = parse_variable(self.config, variable_name)
        self.config.put_value(environment, variable, variable_value)
        self.config.commit()
        return 0


class ChangeEnvironmentCommand(BotControlCommand):
    """Usage
    $ botctl chenv {local | development | production}
    """
    __commandname__ = 'botctl'

    @command_callback
    def __call__(self, environment_name):
        environment = PlatformEnvironment(environment_name.upper())
        self.config.set_environment(environment)
        self.config.commit()
        return 0


def main():
    callbacks = {
        'set': SetCommand,
        'get': GetCommand,
        'del': DelCommand,
        'chenv': ChangeEnvironmentCommand
    }
    return execute_subcommand('botctl', **callbacks)
