from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Image
from .forms import ImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

#ユーザーが保存した画像の一覧を表示する関数
@login_required(login_url='/sns/login/')
def showall(request):

    user = User.objects.filter(email=request.user).first()

    images = Image.objects.all()
    params = {
        'login_user': user.username,
        'images':images
        }
    return render(request, 'album/showall.html', params)

#ユーザーが保存したい画像をアップするための関数
@login_required(login_url='/sns/login/')
def upload(request):
    
    user = User.objects.filter(email=request.user).first()
 
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('album:showall')
    else:
        form = ImageForm()

    params = {
        'login_user': user.username,
        'form':form
        }
    return render(request, 'album/upload.html', params)
        
# Create your views here.
