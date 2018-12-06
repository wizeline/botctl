from botctl.client import BotClientCommand
from botctl.common import command_callback, execute_subcommand


class InstallConversationCommand(BotClientCommand):
    """Usage:
    $ botmod update-conversation {BOT_NAME} < CONVERSATION_FILE.json
    """

    __commandname__ = 'botmod'
    expects_input = True

    @command_callback
    def __call__(self, bot_name):
        self.client.post_conversation(bot_name, self.input)
        return 0


class InstallIntegrationCommand(BotClientCommand):
    """Usage:
    $ botmod install-integration {BOT_NAME} {INTEGRATION_NAME} < CONFIG.json
    """

    __commandname__ = 'botmod'
    expects_input = True

    @command_callback
    def __call__(self, bot_name, integration_name):
        self.client.install_bot_integration(bot_name,
                                            integration_name,
                                            self.input)
        return 0


class InstallNLP(BotClientCommand):
    """Usage:
    $ botmod install-nlp {BOT_NAME} < NLP_CONFIG.json
    """
    __commandname__ = 'botmod'
    expects_input = True

    @command_callback
    def __call__(self, bot_name):
        self.client.install_nlp(bot_name, self.input)
        return 0


def main():
    callbacks = {
        'install-conversation': InstallConversationCommand,
        'install-integration': InstallIntegrationCommand,
        'install-nlp': InstallNLP
    }
    return execute_subcommand('botmod', **callbacks)
