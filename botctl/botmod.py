import sys

from botctl.client import BotClient
from botctl.common import command_callback, display_help
from botctl.config import ConfigStore
from botctl.gateway import BotCMSGateway
from botctl.types import BotControlCommand


class BotModifyCommand(BotControlCommand):
    def set_up(self):
        self.client = BotClient(BotCMSGateway(self.config))


class UpdateConversationCommand(BotModifyCommand):
    """Usage:
    $ botmod update-conversation {BOT_NAME} < CONVERSATION_FILE.json
    """

    __commandname__ = 'update-conversation'

    @command_callback
    def __call__(self, bot_name):
        conversation = sys.stdin.read()
        self.client.post_conversation(bot_name, conversation)


class InstallIntegrationCommand(BotModifyCommand):
    """Usage:
    $ botmod install-integration {BOT_NAME} {INTEGRATION_NAME} < CONFIG.json
    """

    __commandname__ = 'install-integration'

    @command_callback
    def __call__(self, bot_name, integration_name):
        integration = sys.stdin.read()
        print(integration)
        self.client.install_bot_integration(bot_name,
                                            integration_name,
                                            integration)


def main():
    config = ConfigStore()
    command, args = sys.argv[1], sys.argv[2:]

    callbacks = {
        'update-conversation': UpdateConversationCommand(config),
        'install-integration': InstallIntegrationCommand(config)
    }

    if command == 'help':
        action = callbacks.get(args[0])
        sys.exit(display_help(callbacks.get(args[0])))

    else:
        action = callbacks.get(command)
        if action is None:
            sys.stderr.write('Unknown command\n')
            sys.exit(2)
        sys.exit(action(*args))
