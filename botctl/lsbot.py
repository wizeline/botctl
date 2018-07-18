import sys

from botctl.client import BotClient
from botctl.common import command_callback
from botctl.config import ConfigStore
from botctl.gateway import BotCMSGateway


def dump_bot(bot):
    print(bot.get('name'))


@command_callback
def list_bots():
    client = BotClient(
        BotCMSGateway(ConfigStore())
    )

    for bot in client.get_bots():
        dump_bot(bot)


def main():
    sys.exit(list_bots())
