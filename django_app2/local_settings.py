import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '74k529rgv!2j^zjp4y2i0g_wc2+i^2@b+0-c_k@mq$%c_^bs-w'

DEBUG = True

from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)