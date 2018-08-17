import sys

from botctl.client import BotClient
from botctl.common import command_callback
from botctl.config import ConfigStore
from botctl.gateway import BotCMSGateway


def create_bot_client(config):
    return BotClient(BotCMSGateway(config))


@command_callback
def update_conversation(config, bot_name):
    client = create_bot_client(config)
    conversation = sys.stdin.read()
    client.post_conversation(bot_name, conversation)


@command_callback
def install_integration(config, bot_name, integration_name):
    client = create_bot_client(config)
    integration = sys.stdin.read()
    print(integration)
    client.install_bot_integration(bot_name, integration_name, integration)


def main():
    config = ConfigStore()
    command, args = sys.argv[1], sys.argv[2:]

    callbacks = {
        'update-conversation': update_conversation,
        'install-integration': install_integration
    }

    action = callbacks[command]
    sys.exit(action(config, *args))
