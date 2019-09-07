from main.configs.base import Config


class _DevelopmentConfig(Config):
    DEBUG = True


config = _DevelopmentConfig
