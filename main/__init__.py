from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from celery import Celery
from main.config import config

app = Flask(__name__, template_folder='../templates')
app.config.from_object(config)


def _register_subpackages():
    import main.errors
    import main.controllers


# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Initializes the application with the following extensions.
mail = Mail()
mail.init_app(app)

_register_subpackages()

cors = CORS()
cors.init_app(app)
