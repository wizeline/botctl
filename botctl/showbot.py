import sys

from botctl.client import BotClientCommand
from botctl.common import command_callback
from botctl.config import ConfigStore


class ShowBotCommand(BotClientCommand):
    """Usage:
    $ showbot {BOT_NAME}
    """
    __commandname__ = 'showbot'

    @command_callback
    def __call__(self, bot_name):
        bot = self.client.get_by_name(bot_name)
        if bot:
            self.dump_bot(bot)
            return 0
        else:
            sys.stderr.write(f'Bot not found: {bot_name}\n')
            return 1


def main():
    command = ShowBotCommand(ConfigStore())
    if len(sys.argv) != 2:
        print(command.help())
        sys.exit(1)

    bot_name = sys.argv[1]
    sys.exit(command(bot_name))
