from .base import *

INSTALLED_APPS += (
    'debug_toolbar', # and other apps for local development
)

DEBUG = True

#以下local_settingsとの区別は？
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES['default'].update(db_from_env)

#twitter関連
SOCIAL_AUTH_TWITTER_KEY = env('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = env('SOCIAL_AUTH_TWITTER_SECRET')
AUTHENTICATION_TOKEN = env('AUTHENTICATION_TOKEN')
AUTHENTICATION_SECRET = env('AUTHENTICATION_SECRET')
