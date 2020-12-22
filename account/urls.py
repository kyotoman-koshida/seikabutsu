from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('user_change/<int:num>', views.user_change, name='user_change'),
]