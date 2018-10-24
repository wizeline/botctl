class BotControlError(Exception):
    pass


class BotNotFound(BotControlError):
    def __init__(self, bot_name):
        super(BotNotFound, self).__init__(bot_name)

    def __str__(self):
        return f'Bot not found: "{self.args[0]}"'


class UndefinedConfigSection(BotControlError):
    def __init__(self, section):
        self.section = section

    def __str__(self, section):
        return f'Undefined section: [{self.section}]'


class UndefinedConfigValue(BotControlError):
    pass


class GatewayError(BotControlError):
    def __init__(self, response, *args):
        self.response = response

    def __str__(self):
        return self.response.json()['message']


class TokenExpiredError(GatewayError):
    def __str__(self):
        return 'Your session has expired'
