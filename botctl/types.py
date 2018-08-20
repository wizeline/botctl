from enum import Enum


class BotControlEnum(Enum):
    @classmethod
    def values(cls):
        return cls.__members__.values()


class PlatformEnvironment(BotControlEnum):
    LOCAL = 'LOCAL'
    DEVELOPMENT = 'DEVELOPMENT'
    PRODUCTION = 'PRODUCTION'


class PlatformVariable(BotControlEnum):
    ANALYTICS = 'analytics'
    BOT = 'bot'
    CMS = 'cms'
    INTEGRATIONS_MANAGER = 'integrations'
    OPERATIONS = 'operations'
    TOKEN = 'token'


class BotControlCommand:
    __commandname__ = 'command'

    def __init__(self, config):
        self.config = config
        self.set_up()

    def __call__(self):
        raise NotImplementedError(f'{self.__commandname__} is not implemented')

    def help(self):
        return self.__doc__

    def set_up(self):
        pass
