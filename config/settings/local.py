from .base import *

INSTALLED_APPS += (
    'debug_toolbar', # and other apps for local development
)

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_URL = env('DATEBASE_URL')
DATABASES = {
    'default' : env.db(),
}

#twitter関連
SOCIAL_AUTH_TWITTER_KEY = env('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = env('SOCIAL_AUTH_TWITTER_SECRET')
AUTHENTICATION_TOKEN = env('AUTHENTICATION_TOKEN')
AUTHENTICATION_SECRET = env('AUTHENTICATION_SECRET')
