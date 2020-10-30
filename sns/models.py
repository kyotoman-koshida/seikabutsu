from django.db import models
from django.core.validators import ValidationError
from django.contrib.auth.models import User
from django.conf import settings


# Messageクラス
class Message(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
            related_name='message_owner')
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    share_id = models.IntegerField(default=-1)
    good_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.content) + ' (' + str(self.owner) + ')'
    
    def get_share(self):
        return Message.objects.get(id=self.share_id)

    class Meta:
        ordering = ('-pub_date',)

# Groupクラス
class Group(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
            related_name='group_owner')
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

# Friendクラス
class Friend(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
            related_name='friend_owner')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
            related_name='friend_user')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='グループ')

    def __str__(self):
        return str(self.user) + ' (group: "' + str(self.group) + '")'

# Goodクラス
class Good(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
            related_name='good_owner')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.message) + '" (by ' + \
                str(self.owner) + ')'

class Dm(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dm_owner")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dm_user")
    content = models.CharField(max_length=250)
    dm_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content) + " ----DM from " + str(self.owner) + " to " + str(self.user) + \
            str(self.dm_at.month) + "月" + str(self.dm_at.day) + "日"  

    class Meta:
        ordering = ["-dm_at"]                

# Create your models here.
