import sys
import json

from botctl.client import BotClientCommand
from botctl.common import command_callback, display_manual
from botctl.config import ConfigStore

class ReadBotCommand(BotClientCommand):
    '''Usage:
    $ readbot {BOT_NAME}
    $ readbot {BOT_NAME}.{ATTRIBUTE}

    Examples:
      $ readbot myBot.id
      $ readbot myBot.integrations
      $ readbot myBot.users
      $ readbot myBot.customers
      $ readbot myBot.admins
      $ readbot myBot.nlp
      $ readbot myBot.qna
    '''
    __commandname__ = 'readbot'

    @command_callback
    def __call__(self, bot_query):
        result = self._execute(bot_query)

        if isinstance(result, list) or isinstance(result, dict):
            printable_result = json.dumps(result)
        else:
            printable_result = result

        print(printable_result)

    def _execute(self, bot_query):
        bot_name, attribute = self._parse_query(bot_query)
        bot = self.client.get_by_name(bot_name)

        if attribute is None:
            return bot

        if attribute in bot:
            return bot[attribute]

        return self.client.get_attribute(bot, attribute)

    def _parse_query(self, query):
        if '.' not in  query:
            return query, None

        tokens = query.split('.')
        if len(tokens) != 2:
            raise ValueError('readbot', query)

        return tokens[0], tokens[1]


def main():
    if len(sys.argv) != 2:
        display_manual('readbot')
        sys.exit(1)

    command = ReadBotCommand(ConfigStore())
    bot_query = sys.argv[1]
    sys.exit(command(bot_query))
