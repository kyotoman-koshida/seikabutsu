from django.contrib import admin
from django.urls import path, include
from sns.views import index
from django.conf.urls import url

urlpatterns = [
    #/login/twitter/, /complete/twitter/, /disconnect/twitter/に対応
    url('', include('social_django.urls', namespace='social')),

    url('admin/', admin.site.urls),    
    url('sns/',include('sns.urls', namespace='sns')),
    url('', index, name='index'),
    ]