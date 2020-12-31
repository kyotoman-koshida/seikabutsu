
import os
import dj_database_url
import django_heroku

import environ


ROOT_DIR = environ.Path(__file__) - 3  # (django_app2/config/settings/base.py - 3 = modern-django/)

env = environ.Env()

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path('.env')))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com',  'kyotoman-app.herokuapp.com']

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG', False)

DATABASES = {
    'default': env.db()
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'sns',
    'account',
    'album',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'django_app2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', 
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ]
        },
    },
]

WSGI_APPLICATION = 'django_app2.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FILE_CHARSET = 'UTF-8'

AUTH_USER_MODEL = 'account.User'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),  # プロジェクト直下のstaticディレクトリを指定
    'static/',
)

#エラーの内容を送信
ADMINS = (('kyotoman', 'heiheibonbon20120426@gmail.com'),)
MANAGERS = ADMINSEMAIL_HOST = 'host'
SEND_BROKEN_LINK_EMAILS=True

#ログイン関連の設定
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'

#soxial-auth-app-django用
SOCIAL_AUTH_URL_NAMESPACE = 'social'
AUTHENTICATION_BACKENDS = [
    'social_core.backends.twitter.TwitterOAuth',    
    'django.contrib.auth.backends.ModelBackend',    
]

#リダイレクトURL
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/sns'

db_from_env = dj_database_url.config(conn_max_age=500)


