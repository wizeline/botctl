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
