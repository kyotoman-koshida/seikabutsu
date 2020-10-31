# Generated by Django 3.1.1 on 2020-10-31 10:21

import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': 'そのEメールアドレスはすでに使用されています'}, max_length=254, unique=True, verbose_name='Eメール')),
                ('username', models.CharField(help_text='150文字以下。文字と数字と @/./+/-/_ のみ。', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='ユーザ名')),
                ('birthday', models.DateField(blank=True, help_text='例:1996-05-31', null=True, verbose_name='生年月日')),
                ('gender', models.IntegerField(choices=[(1, '男性'), (2, '女性')], verbose_name='性別')),
                ('place', models.CharField(max_length=100, null=True, verbose_name='居住地')),
                ('height', models.FloatField(help_text='男性は170cm未満のかた限定です。', verbose_name='身長')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
