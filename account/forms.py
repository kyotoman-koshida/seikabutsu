from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField 

from .models import User

#ユーザーを新しく作成するためのクラス
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'birthday', 'gender', 'place', 'height', 'user_icon')
        
        def clean(self):
            if self.username == 'dst':#'dst'はDMの送り方を識別するために使うので予約語としておく。
               raise ValidationError("'dstは名前に使えません'")
            if self.gender == 1:
               if self.height < 150.0 or self.height > 169.9:
                   raise ValidationError('身長が170cm以上の男性はご遠慮ください') 

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user  

#ユーザーの登録情報を変更するためのフォーム
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'birthday', 'gender', 'place',
                  'height', 'user_icon', 'is_active', 'is_admin')              

    def clean_password(self):
        return self.initial["password"]