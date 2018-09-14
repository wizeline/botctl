class BotControlError(Exception):
    pass


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
        code = self.response.status_code
        url = self.response.request.url
        body = self.response.text
        return f'Request failed. status [{code}] url [{url}] response [{body}]'


class TokenExpiredError(GatewayError):
    def __str__(self):
        return 'Your session has expired'
