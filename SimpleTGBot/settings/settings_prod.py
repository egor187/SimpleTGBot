from .settings_dev import *


DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = ['*']
