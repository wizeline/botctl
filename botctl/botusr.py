import sys

from botctl.client import BotClientCommand
from botctl.common import command_callback, execute_subcommand


class BotUserLister(BotClientCommand):
    """Usage:
    $ botusr list {BOT_NAME}
    """

    __commandname__ = 'botusr'

    @command_callback
    def __call__(self, bot_name):
        bot = self.client.get_by_name(bot_name)
        if not bot:
            sys.stderr.write(f'Bot not found: {bot_name}\n')
            return 1

        print(self.get_users_table(bot))

        return 0


class InviteUserCommand(BotClientCommand):
    """Usage:
    $ botusr invite {BOT_NAME} {USERS_EMAIL}
    """

    __commandname__ = 'botusr'

    @command_callback
    def __call__(self, bot_name, users_email):
        self.client.invite_user(bot_name, users_email)
        return 0


class UninviteUserCommand(BotClientCommand):
    """Usage
    $ botusr uninvite {BOT_NAME} {USERS_EMAIL}
    """
    __commandname__ = 'botusr'

    @command_callback
    def __call__(self, bot_name, users_email):
        bot = self.client.get_by_name(bot_name)
        if not bot:
            sys.stderr.write(f'Bot not found: {bot_name}\n')
            return 1

        for user in bot['users']:
            if users_email == user['email']:
                self.client.uninvite_user(bot['id'], user['id'])
                return 0

        sys.stderr.write(f'Not a bot user: [{bot_name}] [{users_email}]\n')
        return 1


def main():
    callbacks = {
        'invite': InviteUserCommand,
        'uninvite': UninviteUserCommand,
        'list': BotUserLister
    }
    return execute_subcommand('botusr', **callbacks)
