from django.contrib import admin
from django.urls import path, include
from sns.views import index
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),    
    path('sns/', include('sns.urls', namespace='sns')),
    path('', include('sns.urls', namespace='sns')),
    path('album/', include('album.urls')),
    path('', include('social_django.urls', namespace='social')),

    ] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)