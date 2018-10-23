import sys

from botctl.client import BotClientCommand
from botctl.common import command_callback, execute_subcommand


class UpdateConversationCommand(BotClientCommand):
    """Usage:
    $ botmod update-conversation {BOT_NAME} < CONVERSATION_FILE.json
    """

    __commandname__ = 'botmod'

    @command_callback
    def __call__(self, bot_name):
        conversation = sys.stdin.read()
        self.client.post_conversation(bot_name, conversation)


class InstallIntegrationCommand(BotClientCommand):
    """Usage:
    $ botmod install-integration {BOT_NAME} {INTEGRATION_NAME} < CONFIG.json
    """

    __commandname__ = 'botmod'

    @command_callback
    def __call__(self, bot_name, integration_name):
        integration = sys.stdin.read()
        print(integration)
        self.client.install_bot_integration(bot_name,
                                            integration_name,
                                            integration)


class InstallNLP(BotClientCommand):
    """Usage:
    $ botmod install-nlp {BOT_NAME} < NLP_CONFIG.json
    """
    __commandname__ = 'botmod'

    @command_callback
    def __call__(self, bot_name):
        nlp_config = sys.stdin.read()
        print(nlp_config)
        self.client.install_nlp(bot_name, nlp_config)


class InviteUserCommand(BotClientCommand):
    """Usage:
    $ botmod invite {BOT_NAME} {USERS_EMAIL}
    """

    __commandname__ = 'botmod'

    @command_callback
    def __call__(self, bot_name, users_email):
        bot = self.client.get_by_name(bot_name)
        self.client.invite_user(bot['id'], users_email)


class UninviteUserCommand(BotClientCommand):
    """Usage
    $ botmod uninvite {BOT_NAME} {USERS_EMAIL}
    """
    __commandname__ = 'botmod'

    @command_callback
    def __call__(self, bot_name, users_email):
        bot = self.client.get_by_name(bot_name)
        for user in bot['users']:
            if users_email == user['email']:
                self.client.uninvite_user(bot['id'], user['id'])
                return 0

        sys.stderr.write(f'Not a bot user: [{bot_name}] [{users_email}]\n')
        return 1


def main():
    callbacks = {
        'install-conversation': UpdateConversationCommand,
        'install-integration': InstallIntegrationCommand,
        'install-nlp': InstallNLP,
        'invite': InviteUserCommand,
        'uninvite': UninviteUserCommand
    }
    return execute_subcommand('botmod', **callbacks)
