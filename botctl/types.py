from enum import Enum


class BotControlEnum(Enum):
    @classmethod
    def values(cls):
        return cls.__members__.values()

    @classmethod
    def is_valid(cls, name):
        return name in cls.__members__.keys()


class PlatformEnvironment(BotControlEnum):
    LOCAL = 'LOCAL'
    DEVELOPMENT = 'DEVELOPMENT'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'


class PlatformVariable(BotControlEnum):
    ANALYTICS = 'analytics'
    API_SECRET = 'api_secret'
    BOT = 'bot'
    CMS = 'cms'
    INTEGRATIONS_MANAGER = 'integrations'
    OPERATIONS = 'operations'
    TOKEN = 'token'


class BotControlCommand:
    __commandname__ = 'command'
    expects_input = False

    def __init__(self, config):
        self.config = config
        self.set_up()

    def __call__(self):
        raise NotImplementedError(
            f'{self.__commandname__} is not implemented'
        )

    def help(self):
        return self.__doc__

    def set_up(self):
        pass
