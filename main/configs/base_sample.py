import os


class Config(object):
    DEBUG = False

    # Celery
    CELERY_BROKER_URL = ''
    CELERY_RESULT_BACKEND = ''

    # JWT
    JWT_SECRET = ''
    JWT_LIFE_TIME = 60 * 60 * 24  # seconds
    JWT_ALGORITHMS = ''

    # Google mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # Maximum content capacity is 10MB

    # NeverBounce
    NEVERBOUNCE_API_KEY = ''

    # Imgur
    IMGUR_CLIENT_ID = ''

    # Other
    MAXIMUM_CONFIRMATION_CODE_TRY = 5
