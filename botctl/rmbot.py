import sys

from botctl.client import BotClientCommand
from botctl.common import command_callback, display_manual
from botctl.config import ConfigStore


class BotKiller(BotClientCommand):
    """Usage:
    $ rmbot {BOT_NAME}
    """
    @command_callback
    def __call__(self, bot_name):
        return self.client.destroy_bot(bot_name)


def main():
    if len(sys.argv) < 2:
        display_manual('rmbot')
        sys.exit(1)

    command = BotKiller(ConfigStore())

    for bot_name in sys.argv[1:]:
        command(bot_name)

    sys.exit(0)
