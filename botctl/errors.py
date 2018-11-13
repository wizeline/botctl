class BotControlError(Exception):
    pass


class BotNotFound(BotControlError):
    def __init__(self, bot_name):
        super(BotNotFound, self).__init__(bot_name)

    def __str__(self):
        return f'Bot not found: "{self.args[0]}"'


class InvalidVariableName(BotControlError):
    def __init__(self, variable_name):
        self.variable = variable_name

    def __str__(self):
        return f'Invalid variable: {self.variable}'


class InvalidPlatformEnvironment(BotControlError):
    def __init__(self, environment_name):
        self.environment = environment_name

    def __str__(self):
        return f'Invalid environment: {self.environment}'


class UndefinedConfigSection(BotControlError):
    def __init__(self, section):
        self.section = section

    def __str__(self):
        return f'Undefined section: [{self.section}]'


class UndefinedConfigValue(BotControlError):
    def __init__(self, environment, variable):
        self.environment = environment
        self.variable = variable

    def __str__(self):
        environment = self.environment.value
        variable = self.variable.value

        description = f'Undefined value: {environment}/{variable}'
        hint = f'Run: botctl set {environment.lower()}/{variable} VALUE'

        return f'{description}\n{hint}'


class GatewayError(BotControlError):
    def __init__(self, response, *args):
        self.response = response

    def __str__(self):
        return self.response.json()['message']


class InvalidRemoteHost(GatewayError):
    def __init__(self, host):
        self.host = host

    def __str__(self):
        return f'Invalid remote host {self.host}'

class GatewayConnectionError(GatewayError):
    def __init__(self, host):
        self.host = host

    def __str__(self):
        return f'Could not connect to host {self.host}'

class TokenExpiredError(GatewayError):
    def __str__(self):
        return 'Your session has expired'
