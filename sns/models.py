
from django.db import models
from django.core.validators import ValidationError
from django.contrib.auth.models import User



# Messageクラス
class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='group_owner')
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

      

# Friendクラス
class Friend(models.Model):

    GENDER_CHOICES = (
         (1,'男性'),
         (2,'女性'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='friend_owner')
    user = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='friend_user')
    gender = models.IntegerField(verbose_name='性別',choices=GENDER_CHOICES)     
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='グループ')
    place = models.CharField(max_length=100, verbose_name='居住地')
    introduce = models.CharField(max_length=250, verbose_name='自己紹介', null=True)
    birthday = models.DateTimeField(blank=True, null=True, verbose_name='生年月日')
    height =models.FloatField(verbose_name='身長') 
    
    def clean(self):
        if self.user == 'dst':#'dst'はDMの送り方を識別するために使うので予約語としておく。
            raise ValidationError("'dstは名前に使えません'")
        if self.gender == 1:
            if self.height < 150.0 or self.height > 169.9:
                raise ValidationError('身長が170cm以上の男性はご遠慮ください')


# Goodクラス
class Good(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='good_owner')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.message) + '" (by ' + \
                str(self.owner) + ')'

class Dm(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_owner")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_user")
    content = models.CharField(max_length=250)
    dm_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner) + " が " + str(self.user) + " にDMしました " + \
            str(self.dm_at.month) + "/" + str(self.dm_at.day) + ")"

    class Meta:
        ordering = ["-dm_at"]                

# Create your models here.
