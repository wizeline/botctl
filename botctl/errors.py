class BotControlError(Exception):
    pass


class UndefinedConfigSection(BotControlError):
    pass


class UndefinedConfigValue(BotControlError):
    pass


class GatewayError(BotControlError):
    pass
