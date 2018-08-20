import sys

from botctl.client import BotClientCommand
from botctl.common import command_callback
from botctl.config import ConfigStore


class BotMaker(BotClientCommand):
    """Usage:
    $ mkbot {BOT_NAME}
    """
    @command_callback
    def __call__(self, bot_name):
        return self.client.make_bot(bot_name)


def main():
    command = BotMaker(ConfigStore())
    if len(sys.argv) < 2:
        print(command.help())
        sys.exit(1)

    for bot_name in sys.argv[1:]:
        command(bot_name)

    sys.exit(0)
