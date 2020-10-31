from django.contrib import admin
from django.urls import path, include
from sns.views import index
from django.conf.urls import url

app_name = 'social_django'

urlpatterns = [
    #/login/twitter/, /complete/twitter/, /disconnect/twitter/に対応
    path('', include('social_django.urls')),
    url('admin/', admin.site.urls),    
    url('sns/',include('sns.urls', namespace='sns')),
    url('', index, name='top'),
    ]
