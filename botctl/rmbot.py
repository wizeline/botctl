import sys

from botctl.client import BotClientCommand
from botctl.common import command_callback
from botctl.config import ConfigStore


class BotKiller(BotClientCommand):
    """Usage:
    $ rmbot {BOT_NAME}
    """
    @command_callback
    def __call__(self, bot_name):
        return self.client.destroy_bot(bot_name)


def main():
    command = BotKiller(ConfigStore())
    if len(sys.argv) < 2:
        print(command.help())
        sys.exit(1)

    for bot_name in sys.argv[1:]:
        command(bot_name)

    sys.exit(0)
