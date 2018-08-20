import sys

from botctl.client import BotClientCommand
from botctl.common import command_callback
from botctl.config import ConfigStore


class BotLister(BotClientCommand):
    """Usage:
    $ lsbot
    """
    @command_callback
    def __call__(self):
        for bot in self.client.get_bots():
            self.dump_bot_name(bot)


def main():
    command = BotLister(ConfigStore())

    if len(sys.argv) > 1:
        print(command.help())
        sys.exit(1)

    sys.exit(command())
