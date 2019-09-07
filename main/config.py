import os
from importlib import import_module

env = os.getenv('FLASK_ENV', 'development')
if not env in ['development', 'production']:
    config_file = 'main/configs/' + env + '.py'
    if not os.path.isfile(config_file):
        env = 'development'

config_name = 'main.configs.' + env
module = import_module(config_name)
config = module.config
