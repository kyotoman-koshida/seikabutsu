from .base import *

DEBUG = False

DATABASE_URL = env('DATEBASE_URL')
DATABASES = {
    'default': env.db()
}

#シークレットキー
SECRET_KEY = os.environ['SECRET_KEY']

#メール送信について
EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']

DATABASES = {
    'default': {
        'ENGINE': os.environ['POSTGRES_ENGINE'],
        'NAME': os.environ['POSTGRES_NAME'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD':os.environ['POSTGRES_PASSWORD'],
        'HOST':os.environ['POSTGRES_HOST'],
        'PORT':os.environ['POSTGRES_PORT'],
    }
}
DATABASES['default'].update(db_from_env)

#TwitterのAPI関連
SOCIAL_AUTH_TWITTER_KEY = os.environ['SOCIAL_AUTH_TWITTER_KEY']
SOCIAL_AUTH_TWITTER_SECRET = os.environ['SOCIAL_AUTH_TWITTER_SECRET']
AUTHENTICATION_TOKEN = os.environ['AUTHENTICATION_TOKEN']
AUTHENTICATION_SECRET = os.environ['AUTHENTICATION_SECRET']
#django_heroku.settings(locals())


   
