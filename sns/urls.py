from django.conf import settings
from django.conf.urls import url
from django.urls import path
from social_core.utils import setting_name
from . import views
from social_django import views as social_views

app_name = 'sns'
extra = getattr(settings, setting_name('TRAILING_SLASH'), True) and '/' or ''

urlpatterns = [
    path('', views.index, name='index'),
    path('groups', views.groups, name='groups'),
    path('add', views.add, name='add'),
    path('creategroup', views.creategroup, name='creategroup'),
    path('post', views.post, name='post'),
    path('share/<int:share_id>', views.share, name='share'),
    path('good/<int:good_id>', views.good, name='good'),
    path('notifications', views.notifications, name='notifications'),#未使用
    path('mypage', views.mypage, name='mypage'),
    path('otherspage', views.otherspage, name='otherspage'),
    path('dm', views.dm, name='dm'),
    path('settings', views.settings, name='settings'), #アプリ登録などを行うsettingsフォルダとは無関係
    path('blocks', views.blocks, name='blocks'),#未使用
    path('goods', views.goods, name='goods'),#未使用
    path('all_users', views.all_users, name='all_users'),
    path('all_friends', views.all_friends, name='all_friends'),
    #path('top/', views.Top.as_view(), name='top'),
    path('top/', views.top_page, name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('twitter/', views.twitter, name='twitter'),
    path('addtweet/', views.addtweet, name='addtweet'),      
]