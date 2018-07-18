import sys

from botctl.client import BotClient
from botctl.common import command_callback
from botctl.config import ConfigStore
from botctl.gateway import BotCMSGateway


def dump_bot(bot):
    print(bot.get('name'))


@command_callback
def make_bot(config, bot_name):
    client = BotClient(BotCMSGateway(config))
    return client.make_bot(bot_name)


def main():
    bot_name = sys.argv[1]
    config = ConfigStore()
    sys.exit(make_bot(config, bot_name))
