from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

#ユーザーが自身の登録情報を自分で変更するときのための関数
@login_required(login_url='/sns/login/')
def user_change(request, num):

    obj = User.objects.get(id=num)
    me = User.objects.filter(email=request.user).first()
    user = UserCreationForm(request.POST, instance=obj)
    
    if (request.method == 'POST'):
        '''
        obj.is_admin = me.is_admin
        obj.is_staff = me.is_staff
        obj.is_active = me.is_active
        obj.date_joined = me.date_joined
        
        obj.gender = me.gender
        obj.password = me.password
        '''
        
        user = UserCreationForm(request.POST, instance=obj)
        
        if user.is_valid():
           user.save()
          
        return redirect(to='/sns/mypage')   
    
    #変更フォームに現在の登録情報を表示するための辞書
    initial_dict = {
        'email': request.user,
        'username': obj.username,
        'birthday': obj.birthday,
        'place': obj.place,
        'height': obj.height,
        'user_icon': obj.user_icon,
    }

    params = {
        'login_user': obj.username,
        'form': UserCreationForm(instance=obj, initial=initial_dict),
        'id': num,
        'user':user,
    }

    return render(request, 'account/user_change.html', params)