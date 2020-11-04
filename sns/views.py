
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings as conf_settings

User = conf_settings.AUTH_USER_MODEL
from django.contrib import messages
from .models import Message,Friend,Group,Good,Dm
from .forms import GroupCheckForm,GroupSelectForm,\
        SearchForm,FriendsForm,CreateGroupForm,PostForm,\
            DMForm, LoginForm, UserCreateForm, UserCheckForm,\
                LoginForm, UserCreateForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404, HttpResponseBadRequest
from django.views import generic
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from social_django.models import UserSocialAuth
from requests_oauthlib import OAuth1Session
import json
import re
import time, calendar
import datetime
import os
import requests
import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

# indexのビュー関数
@login_required(login_url='/sns/login/')
def index(request):
    
    # publicのuserを取得
    (public_user, public_group) = get_public()

    # POST送信時の処理
    if request.method == 'POST':

        # Groupsのチェックを更新した時の処理
        if request.POST['mode'] == '__check_form__':
            # フォームの用意
            searchform = SearchForm()
            checkform = GroupCheckForm(request.user,request.POST)
            # チェックされたGroup名をリストにまとめる
            glist = []
            for item in request.POST.getlist('groups'):
                glist.append(item)
            # Messageの取得
            messages = get_your_group_message(request.user, \
                    glist, None)

        # Groupsメニューを変更した時の処理   
        if request.POST['mode'] == '__search_form__':
            # フォームの用意
            searchform = SearchForm(request.POST)
            checkform = GroupCheckForm(request.user)
            # Groupのリストを取得
            gps = Group.objects.filter(owner=request.user)
            glist = [public_group]
            for item in gps:
                glist.append(item)
            # メッセージを取得
            messages = get_your_group_message(request.user, glist, \
                    request.POST['search'])

    # GETアクセス時の処理
    else:
        # フォームの用意
        searchform = SearchForm()
        checkform = GroupCheckForm(request.user)
        # Groupのリストを取得
        gps = Group.objects.filter(owner=request.user)
        glist = [public_group]
        for item in gps:
            glist.append(item)
        # メッセージの取得
        messages = get_your_group_message(request.user, glist, None)

    #　共通処理
    params = {
            'login_user':request.user,
            'contents':messages,
            'check_form':checkform,
            'search_form':searchform,
        }
    return render(request, 'sns/index.html', params)

@login_required(login_url='/sns/login/')
def groups(request):
    # 自分が登録したFriendを取得
    friends = Friend.objects.filter(owner=request.user)
    groupsform = GroupSelectForm(request.user)
    friendsform = FriendsForm(request.user, friends=friends, \
                vals=[])
    sel_group = '-'            
    
    # POST送信時の処理
    if request.method == 'POST':
        
        # Groupsメニュー選択肢の処理
        if request.POST['mode'] == '__groups_form__':
            # 選択したGroup名を取得
            sel_group = request.POST['groups']
            # Grooupを取得
            gp = Group.objects.filter(owner=request.user) \
                .filter(title=sel_group).first()
            # Groupに含まれるFriendを取得
            fds = Friend.objects.filter(owner=request.user) \
                .filter(group=gp)
            # FriendのUserをリストにまとめる
            vlist = []
            for item in fds:
                vlist.append(item.user.username)
            # フォームの用意
            groupsform = GroupSelectForm(request.user,request.POST)
            friendsform = FriendsForm(request.user, \
                    friends=friends, vals=vlist)
        
        # Friendsのチェック更新時の処理
        if request.POST['mode'] == '__friends_form__':
            # 選択したGroupの取得
            sel_group = request.POST['group']
            group_obj = Group.objects.filter(title=sel_group).first()
            # チェックしたFriendsを取得
            sel_fds = request.POST.getlist('friends')
            # FriendsのUserを取得
            sel_users = User.objects.filter(username__in=sel_fds)
            # Userのリストに含まれるユーザーが登録したFriendを取得
            fds = Friend.objects.filter(owner=request.user) \
                    .filter(user__in=sel_users)
            # すべてのFriendにGroupを設定し保存する
            vlist = []
            for item in fds:
                item.group = group_obj
                item.save()
                vlist.append(item.user.username)
            # メッセージを設定
            messages.success(request, ' チェックされたFriendを' + \
                    sel_group + 'に登録しました。')
            # フォームの用意
            groupsform = GroupSelectForm(request.user, \
                    {'groups':sel_group})
            friendsform = FriendsForm(request.user, \
                    friends=friends, vals=vlist)
     
    # 共通処理
    createform = CreateGroupForm()
    params = {
            'login_user':request.user,
            'groups_form':groupsform,
            'friends_form':friendsform,
            'create_form':createform,
            'group':sel_group,
        }
    return render(request, 'sns/groups.html', params)

# Friendの追加処理
@login_required(login_url='/sns/login/')
def add(request):
    # 追加するUserを取得
    add_name = request.GET['name']
    add_user = User.objects.filter(email=add_name).first()
    # Userが本人だった場合の処理
    if add_user == request.user:
        messages.info(request, "自分自身をFriendに追加することは\
                できません。")
        return redirect(to='/sns')
    # publicの取得
    (public_user, public_group) = get_public()
    # add_userのFriendの数を調べる
    frd_num = Friend.objects.filter(owner=request.user) \
            .filter(user=add_user).count()
    # ゼロより大きければ既に登録済み
    if frd_num > 0:
        messages.info(request, add_user.username + \
                ' は既に追加されています。')
        return redirect(to='/sns')
    
    # ここからFriendの登録処理
    frd = Friend()
    frd.owner = request.user
    frd.user = add_user
    frd.group = public_group
    frd.save()
    # メッセージを設定
    messages.success(request, add_user.username + ' を追加しました！\
        groupページに移動して、追加したFriendをメンバーに設定して下さい。')
    return redirect(to='/sns')

# グループの作成処理
@login_required(login_url='/sns/login/')
def creategroup(request):
    # Groupを作り、Userとtitleを設定して保存する
    gp = Group()
    gp.owner = request.user
    gp.title = request.POST['group_name']
    gp.save()
    messages.info(request, '新しいグループを作成しました。')
    return redirect(to='/sns/groups')

# メッセージのポスト処理
@login_required(login_url='/sns/login/')
def post(request):
    # POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        gr_name = request.POST['groups']
        content = request.POST['content']
        # Groupの取得
        group = Group.objects.filter(owner=request.user) \
                .filter(title=gr_name).first()
        if group == None:
            (pub_user, group) = get_public()
        # Messageを作成し設定して保存
        msg = Message()
        msg.owner = request.user
        msg.group = group
        msg.content = content
        msg.save()
        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns/')
    
    # GETアクセス時の処理
    else:
        form = PostForm(request.user)
    
    # 共通処理
    params = {
            'login_user':request.user,
            'form':form,
        }
    return render(request, 'sns/post.html', params)

# 投稿をシェアする
@login_required(login_url='/sns/login/')
def share(request, share_id):
    # シェアするMessageの取得
    share = Message.objects.get(id=share_id)
    #print(share)
    # POST送信時の処理
    if request.method == 'POST':
        # 送信内容を取得
        gr_name = request.POST['groups']
        content = request.POST['content']
        # Groupの取得
        group = Group.objects.filter(owner=request.user) \
                .filter(title=gr_name).first()
        if group == None:
            (pub_user, group) = get_public()
        # メッセージを作成し、設定をして保存
        msg = Message()
        msg.owner = request.user
        msg.group = group
        msg.content = content
        msg.share_id = share.id
        msg.save()
        share_msg = msg.get_share()
        share_msg.share_count += 1
        share_msg.save()
        # メッセージを設定
        messages.success(request, 'メッセージをシェアしました！')
        return redirect(to='/sns')
    
    # 共通処理
    form = PostForm(request.user)
    params = {
            'login_user':request.user,
            'form':form,
            'share':share,
        }
    return render(request, 'sns/share.html', params)

# goodボタンの処理
@login_required(login_url='/sns/login/')
def good(request, good_id):
    # goodするMessageを取得
    good_msg = Message.objects.get(id=good_id)
    # 自分がメッセージにGoodした数を調べる
    is_good = Good.objects.filter(owner=request.user) \
            .filter(message=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        messages.success(request, '既にメッセージにはGoodしています。')
        return redirect(to='/sns')
    
    # Messageのgood_countを１増やす
    good_msg.good_count += 1
    good_msg.save()
    # Goodを作成し、設定して保存
    good = Good()
    good.owner = request.user
    good.message = good_msg
    good.save()
    # メッセージを設定
    messages.success(request, 'メッセージにGoodしました！')
    return redirect(to='/sns')

#自分のマイページを表示
@login_required(login_url='/sns/login/')
def mypage(request):
    #自分の情報を表示
    me = User.objects.filter(email=request.user).first()
    params = {
         'my_user':me,
    }
    return render(request, "sns/mypage.html", params)

@login_required(login_url='/sns/login/')
def otherspage(request):
    #マイページを開きたいFriendの情報を取得
    fri_name = request.GET['name']
    friend = User.objects.filter(username=fri_name).first()
    params = {    
         'friend':friend,
    }       
    return render(request, "sns/otherspage.html", params)

#DMのための処理
@login_required(login_url='/sns/login/')
def dm(request):
    #markはDMをおくるときにプルダウンから宛先を選ぶ場合を識別するためにdm.htmlに送る値
    mark = 0
    #DMでやりとりした内容を取得    
    dialogs = Dm.objects.filter(Q(owner=request.user) | Q(user=request.user))    
    #自分が追加したFriendの名前を選択できるようにformに入れる
    myfris = Friend.objects.filter(owner=request.user)
    #myfris2 = User.objects.filter(username=myfris.user)
    #エラー回避のためにさきに定義しておく
    fri_name = ''

    form = DMForm()  

    #DMフォームを記入して送信するときの操作
    if request.method == "POST":
        
        obj = Dm()
        dms = DMForm(request.POST, instance=obj)
        if request.POST.get('mode') == '__dm_form__':#'mode'の値が__dm_form__のときはDMのあてさきがプルダウンからされた場合。
            dms.fields['user'].choices = [
                ("----", "----")
                ] + [
                (item.user, item.user) for item in myfris
               ]
            #DMの受け取り主を取得
            obj.owner = User.objects.filter(email=request.POST.get('user')).first()   
            
        else:       
            fri_name = request.POST.get('mode')#'mode'の値はDMのあてさきが入っている。
            dms.fields['user'].choices = [
                (fri_name, fri_name)
            ]
            obj.owner = User.objects.filter(username=fri_name).first()

        #DMの送り主を取得
        obj.user = User.objects.filter(email=request.user).first()
        
        
        if dms.is_valid():
           dms.save()
        
        form.fields['user'].choices = [
            ("----", "----")
            ] + [
            (item.user, item.user) for item in myfris
            ]
        
                
    #Friendのマイページからとんできた場合
    elif request.GET['name'] != 'dst' :#dstはdestination DMの宛先が未定のときと区別する
        fri_name = request.GET['name']
        form.fields['user'].choices = [
            (fri_name, fri_name)
        ]
          
    else:           
          
        form.fields['user'].choices = [
            ("----", "----")
            ] + [
            (item.user, item.user) for item in myfris
            ]
        #mark=1のときはプルダウンでフレンドを選ぶとき    
        mark = 1       
    
    params = {
        "dialogs":dialogs,
        "dm_form":form,
        "mark": mark,
        "atesaki": fri_name,
    }
    return render(request, "sns/dm.html", params)

#通知ページを表示(未使用)
@login_required(login_url='/sns/login/')
def notifications(request):
    params = {
        'note':request.user,
    }
    return render(request, "sns/notifications.html", params)

#自身の設定ページを表示(未使用)
@login_required(login_url='/sns/login/')
def settings(request):
    params = {
          'name':request.user,
    }   
    return render(request, "sns/settings.html", params)

#グッドしたものの一覧を表示(未使用)
@login_required(login_url='/sns/login/')
def goods(request):
    return(request, 'sns/goods.html')

#ブロックしたフレンドを表示（未使用）
@login_required(login_url='/sns/login/')
def blocks(request):
    return('sns/blocks.html')

#このサービスに登録しているユーザを列挙する
@login_required(login_url='/sns/login/')
def all_users(request):

    if request.method == 'POST':
        # Groupsメニュー選択肢の処理
        if request.POST['mode'] == '__allusers_form__':
            
            vlist = []  
            # FriendのUserをリストにまとめる
            for item in users:
                vlist.append(item.username)
            
            #ユーザ選択フォームの用意
            usersform = UserCheckForm(request.user, request.POST)
      
    # GETアクセス時の処理  
    else:
        # フォームの用意
        usersform = UserCheckForm(request.user,request.POST)
        me = User.objects.filter(email=request.user).first()     
        #全異性ユーザを取得
        if me.gender == 1:
            users = User.objects.filter(gender=2)
        else:
            users = User.objects.filter(gender=1)

    params = {
        'usersform':usersform,
        'users':users,
        'me':me,
    }
    return render(request, 'sns/all_users.html', params)          

#自分の登録しているフレンドを列挙する
@login_required(login_url='/sns/login/')
def all_friends(request):
    fri_user_list = []
    me = User.objects.filter(email=request.user).first()
    if request.method == 'POST':
        # Groupsメニュー選択肢の処理
        if request.POST['mode'] == '__groups_form__':
            # フォームのメニューで選択したGroup名を取得
            sel_group = request.POST['groups']
            # Grooupを取得
            gp = Group.objects.filter(owner=request.user) \
                .filter(title=sel_group).first()

            # Groupに含まれるFriendを取得（デフォルトは全フレンドの表示）
            if sel_group == '-':
               myfri =Friend.objects.all()
            else:
                myfri = Friend.objects.filter(owner=request.user) \
                .filter(group=gp)

            
            # FriendのUserをリストにまとめる
            
            for item in myfri:
                if me.gender == 1:
                    fri_user = User.objects.filter(email=item.user).filter(gender=2).first()
                else:
                    fri_user = User.objects.filter(email=item.user).filter(gender=1).first()
                fri_user_list.append(fri_user)
            #フォームの用意
            groupsform = GroupSelectForm(request.user, request.POST)
      
    # GETアクセス時の処理  
    else:
        myfri = Friend.objects.filter(owner=request.user)
        # FriendのUserをリストにまとめる    
        for item in myfri:
            if me.gender == 1:
                fri_user = User.objects.filter(email=item.user).filter(gender=2).first()
            else:
                fri_user = User.objects.filter(email=item.user).filter(gender=1).first()
            fri_user_list.append(fri_user)
        # フォームの用意
        groupsform = GroupSelectForm(request.user,request.POST)
        gp = Group.objects.all()
        sel_group = '-'
    
    params = {
            'groups_form':groupsform,
            'group':gp,
            'friends':fri_user_list,
            'gpname':sel_group,
            'me':me,
        }

    return render(request, 'sns/all_friends.html', params)

def twitter(request):
    
    msg = request.GET.get('words')

    C_KEY = conf_settings.SOCIAL_AUTH_TWITTER_KEY
    C_SECRET = conf_settings.SOCIAL_AUTH_TWITTER_SECRET
    A_KEY = conf_settings.AUTHENTICATION_TOKEN
    A_SECRET = conf_settings.AUTHENTICATION_SECRET

    url = 'https://api.twitter.com/1.1/statuses/update.json'
    params = {
        'status': msg,
        'lang': 'ja'
        }

    #req = tw.post(url, params = params)
    user = UserSocialAuth.objects.get(user_id=request.user.id)
    tw = OAuth1Session(C_KEY,C_SECRET,user.access_token['oauth_token'],user.access_token['oauth_token_secret'])
    url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
    params = {'count': 5}
    req = tw.get(url, params = params)

    if req.status_code == 200:
        timeline = json.loads(req.text)
        limit = req.headers['x-rate-limit-remaining']
        
        
        
        #tweet情報をリストにまとめる
        Textlist = []
        Userlist = []
        Namelist = []
        Imglist = []
        Cre_at_list = []

        for tweet in timeline:
            Text = (tweet['text'])
            Textlist.append(Text)
            twi_User = (tweet['user']['screen_name'])
            Userlist.append(twi_User)
            Name = (tweet['user']['name'])
            Namelist.append(Name)
            Img = (tweet['user']['profile_image_url'])
            Imglist.append(Img)
            Created_at = YmdHMS(tweet['created_at'])
            Cre_at_list.append(Created_at)
    
            #tweetの保存されるグループを指定
            gr_name = 'public'
            group = Group.objects.filter(owner=request.user) \
                    .filter(title=gr_name).first()
            if group == None:
                (pub_user, group) = get_public()
            

            #tweetをデータベースにMessageとして保存する
            msg = Message()
            msg.content = Text
            msg.owner = User.objects.filter(email=user).first()
            msg.group = group
            msg.save()
        
        #tweet情報のまとめ
        params = {
            'Words': msg,
            'timeline': timeline,
            'API_limit': limit,
            'user': user,
            'req':req.text,
            }
        return render(request, 'sns/tweets.html', params)

    else:
        Error = {
            'Error_message': 'API制限中',
        }
        return render(request, 'sns/tweets.html', Error)           

def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return int(time.strftime('%Y%m%d%H%M%S', time_local))

#トップページを表示(未使用)
@login_required(login_url='/sns/login/')
def top_page(request):
    user = UserSocialAuth.objects.get(user_id=request.user.id)

    return render(request,'sns/top.html',{'user': user})        

#ログインページを表示
class Login(LoginView):
    form_class = LoginForm
    template_name = 'sns/login.html'    

#ログアウトページを表示
class Logout(LogoutView):
    template_name = 'sns/logout.html'

#ユーザー仮登録
class UserCreate(generic.CreateView):
    template_name = 'sns/user_create.html'
    form_class = UserCreateForm

    #仮登録と本登録のメール発行top
    def form_valid(self, form):
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        params = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('sns/mail_template/create/subject.txt', params)
        message = render_to_string('sns/mail_template/create/message.txt', params)

        user.email_user(subject, message)
        return redirect('sns:user_create_done')

#仮登録の完了クラス
class UserCreateDone(generic.TemplateView):
    template_name = 'sns/user_create_done.html'

#メールから本登録に進んだ時の処理
class UserCreateComplete(generic.TemplateView):
    template_name = 'sns/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    #tokrnが正しければ本登録
    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()        


# これ以降はビュー関数ではなく普通の関数==================

# 指定されたグループおよび検索文字によるMessageの取得
def get_your_group_message(owner, glist, find):
    # publicの取得
    (public_user,public_group) = get_public()
    # チェックされたGroupの取得
    groups = Group.objects.filter(Q(owner=owner) \
            |Q(owner=public_user)).filter(title__in=glist)
    # Groupに含まれるFriendの取得
    me_friends = Friend.objects.filter(group__in=groups)
    # FriendのUserをリストにまとめる
    me_users = []
    for f in me_friends:
        me_users.append(f.user)
    # UserリストのUserが作ったGroupの取得
    his_groups = Group.objects.filter(owner__in=me_users)
    his_friends = Friend.objects.filter(user=owner) \
            .filter(group__in=his_groups)
    me_groups = []
    for hf in his_friends:
        me_groups.append(hf.group)
    # groupがgroupsに含まれるか、me_groupsに含まれるMessageの取得
    if find==None:
        messages = Message.objects.filter(Q(group__in=groups) \
            |Q(group__in=me_groups))[:100]
    else:
        messages = Message.objects.filter(Q(group__in=groups) \
            |Q(group__in=me_groups)) \
            .filter(content__contains=find)[:100]
    return messages

# publicなUserとGroupを取得する
def get_public():
    public_user = User.objects.filter(username='public').first()
    all_fri__group = Group.objects.filter(owner=public_user).first()
    return (public_user, all_fri__group)

#ユーザ検索のための関数(未使用)
def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        if q_word:
            object_list = User.objects.filter(
                Q(title__icontains=q_word) | Q(author__icontains=q_word))
        else:
            object_list = User.objects.all()
        params = {
            'objects_list':object_list,
            'q_word':q_word,
        }    
        return params

