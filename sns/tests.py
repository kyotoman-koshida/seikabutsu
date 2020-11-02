from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Message, Group
from django.contrib.auth import get_user_model
User = get_user_model()

class SnsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        (usr, grp) = cls.create_user_and_group()
        cls.create_message(usr, grp)

    @classmethod
    def create_user_and_group(cls):
        # Create public user & public group.
        User(username="public", password="public", is_staff=False, is_active=True).save()
        pb_usr = User.objects.filter(username='public').first()
        Group(title='public',owner_id=pb_usr.id).save()
        pb_grp = Group.objects.filter(title='public').first()

        # Create test user
        User(username="test", password="test", is_staff=True, is_active=True).save()
        usr = User.objects.filter(username='test').first()

        return (usr, pb_grp)

    @classmethod
    def create_message(cls, usr, grp):
        #Create test message
        Message(content='this is test message.', owner_id=usr.id, group_id=grp.id).save()
        Message(content='test', owner_id=usr.id, group_id=grp.id).save()
        Message(content="OK", owner_id=usr.id, group_id=grp.id).save()
        Message(content="ng", owner_id=usr.id, group_id=grp.id).save()
        Message(content='finish', owner_id=usr.id, group_id=grp.id).save()

    def test_check(self):
        usr = User.objects.filter(username='test').first()

        # access to SNS
        response = self.client.get(reverse('index'))
        self.assertIs(response.status_code, 302)

        #login test account and access to SNS.
        self.client.force_login(usr)
        response = self.client.get(reverse('index'))
        self.assertIs(response.status_code, 200)
        self.assertContains(response, 'this is test message.')

# Create your tests here.
