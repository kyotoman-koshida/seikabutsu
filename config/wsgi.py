"""
WSGI config for django_app2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
"""
#settings.pyをテストと本番環境用に区別するため変更
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app2.settings')
"""
#新settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
application = get_wsgi_application()

from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)