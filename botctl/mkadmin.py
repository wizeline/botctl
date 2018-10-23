import sys

from botctl.common import command_callback, display_manual
from botctl.config import ConfigStore
from botctl.client import BotClientCommand


class AdminMakerCommand(BotClientCommand):
    """Usage:
    $ mkadmin {BOT_NAME} {USERS_EMAIL}
    """

    __commandname__ = 'mkadmin'

    @command_callback
    def __call__(self, bot_name, users_email):
        bot = self.client.get_by_name(bot_name)
        for user in bot['users']:
            if user['email'] == users_email:
                if user['role'] == 'admin':
                    sys.stderr.write(
                        f'User {users_email} is an admin already\n'
                    )
                    return 1

                self.client.make_admin(bot['id'], user['id'])
                return 0
        sys.stderr.write(f'Not a bot user: {bot_name} [{users_email}]\n')
        return 2


def main():
    if len(sys.argv) != 3:
        display_manual('mkadmin')
    else:
        command = AdminMakerCommand(ConfigStore())
        rc = command(sys.argv[1], sys.argv[2])
        if rc != 0:
            command.help()
        sys.exit(rc)
