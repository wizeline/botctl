import json
import sys

from botctl.client import BotClient
from botctl.common import command_callback
from botctl.config import ConfigStore
from botctl.gateway import BotCMSGateway


@command_callback
def show_bot(config, bot_name):
    client = BotClient(BotCMSGateway(config))
    bot = client.get_by_name(bot_name)
    if bot:
        print(json.dumps(bot, indent=2))
        return 0
    else:
        sys.stderr.write(f'Bot not found: {bot_name}\n')
        return 1


def main():
    bot_name = sys.argv[1]
    config = ConfigStore()
    sys.exit(show_bot(config, bot_name))
