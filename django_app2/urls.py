from django.contrib import admin
from django.urls import path, include
from sns.views import index
from django.conf.urls import url

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('sns/', include('sns.urls')),
    #path('', include('sns.urls')),

    #/login/twitter/, /complete/twitter/, /disconnect/twitter/に対応
    path('', include('social_django.urls')),
    #path('user/', include('social_django.urls', namespace='social')),

    url('admin/', admin.site.urls),    
    url('sns/',include('sns.urls', namespace='sns')),
    url('', index, name='top'),
    #path('user/', include('sns.urls')),
    ]
