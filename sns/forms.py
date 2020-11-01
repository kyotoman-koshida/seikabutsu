from django import forms
from.models import Message,Group,Friend,Good, Dm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)

# Messageのフォーム（未使用）
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['owner','group','content']
# Groupのフォーム（未使用）
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['owner', 'title']
# Friendのフォーム（未使用）
class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['owner', 'user', 'group']
# Goodのフォーム（未使用）
class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['owner', 'message']

# 検索フォーム(未使用)
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)

# Groupのチェックボックスフォーム
class GroupCheckForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupCheckForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='public').first()
        self.fields['groups'] = forms.MultipleChoiceField(
            choices=[(item.title, item.title) for item in \
                 Group.objects.filter(owner__in=[user,public])],
            widget=forms.CheckboxSelectMultiple(),
        )

# ユーザー選択のためのチェックボックスフォーム（未使用）
class UserCheckForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(UserCheckForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.MultipleChoiceField(
            choices=[(item.username, item.username) for item in User.objects.all()],
            widget=forms.CheckboxSelectMultiple(),
        )        

# Groupの選択メニューフォーム
class GroupSelectForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupSelectForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) \
                 for item in Group.objects.filter(owner=user)],
        )

# Friendのチェックボックスフォーム
class FriendsForm(forms.Form):
    def __init__(self, user, friends=[], vals=[], *args, **kwargs):
        super(FriendsForm, self).__init__(*args, **kwargs)
        self.fields['friends'] = forms.MultipleChoiceField(
            choices=[(item.user, item.user) for item in friends],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals
        )

# Group作成フォーム
class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=50)

# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=280, \
            widget=forms.Textarea, \
            help_text='280文字までです。'
                )
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='public').first()
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) \
                     for item in Group.objects. \
                     filter(owner__in=[user,public])],
        )

#DMのためのフォーム
class DMForm(forms.ModelForm):
    #選択肢の中からDMの送信先を決定
    user = forms.fields.ChoiceField(widget=forms.widgets.Select)
    class Meta:
        model = Dm
        fields = ['content']

#ログインのためのフォーム
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label        

#ユーザ登録用フォーム
class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'username', 'birthday', 'gender', 'place', 'height')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

    