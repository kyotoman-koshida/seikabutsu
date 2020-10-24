from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import ValidationError

class UserManager(BaseUserManager):
    #use_in_migrations = True

    def create_user(self, email, username, birthday, gender, place, height, password=None):
        """
        Create and save a user with the given username, email, gender, place, birthday and password.
        """
        if not email:
            raise ValueError('メールアドレスは設定してください')
        
        
        user=self.model(
            email = self.normalize_email(email),
            username = self.model.normalize_username(username),
            birthday = birthday,
            gender = gender,  
            place = place,
            height = height,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, birthday, gender, place, height, password):
        user=self.create_user(
            email,
            password=password,
            username = username,
            birthday = birthday,
            gender = gender,  
            place = place,
            height = height,            
        )
        user.is_admin=True
        user.is_staff=True
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    email = models.EmailField(
        unique=True, 
        error_messages={
            'unique': _("そのEメールアドレスはすでに使用されています"),
        },
        verbose_name='Eメール'
        )
    

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,        
        validators=[username_validator],
        help_text=_('150文字以下。文字と数字と @/./+/-/_ のみ。'),
        verbose_name='ユーザ名'       
    )

    birthday = models.DateField(
        blank=True, 
        null=True, 
        help_text=_('例:1996-05-31'),
        verbose_name='生年月日'
    )    

    GENDER_CHOICES = (
         (1,'男性'),
         (2,'女性'),
    )
    gender = models.IntegerField(verbose_name='性別',choices=GENDER_CHOICES)
    place = models.CharField(max_length=100, verbose_name='居住地', null=True)
    #introduce = models.CharField(max_length=250, verbose_name='自己紹介', null=True)
    height =models.FloatField(help_text=_('男性は170cm未満のかた限定です。'), verbose_name='身長')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='登録日')

    

    #is_staff = models.BooleanField(
    #    _('staff status'),
    #    default=False,
    #    help_text=_('Designates whether the user can log into this admin site.'),
    #)
    is_active = models.BooleanField(
        _('active'),
        default=True,
           )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'birthday', 'gender', 'place', 'height']

    #class Meta:
    #    verbose_name = _('user')
    #    verbose_name_plural = _('users')
    #   #abstract = True # ここを削除しないといけないことを忘れない！！！！！！！！！！
    #    swappable = 'AUTH_USER_MODEL'

    
    def clean(self):
        if self.username == 'dst':#'dst'はDMの送り方を識別するために使うので予約語としておく。
            raise ValidationError("'dstは名前に使えません'")
        if self.gender == 1:
            if self.height < 150.0 or self.height > 169.9:
                raise ValidationError('身長が170cm以上の男性はご遠慮ください')    

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    #def get_full_name(self):
    #    """
    #    Return the first_name plus the last_name, with a space in between.
    #    """
    #    full_name = '%s %s' % (self.first_name, self.last_name)
    #    return full_name.strip()
    #def get_short_name(self):
    #    """Return the short name for the user."""
    #    return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    #@property
    #def is_staff(self):
    #   return self._is_admin    

# Create your models here.
