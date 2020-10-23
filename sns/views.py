
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
#from django.contrib.auth.models import User
from django.conf import settings
#ユーザーはカスタムユーザーに変更
User = settings.AUTH_USER_MODEL
#from django.contrib.auth import get_user_model as user_model
#User = user_model()

from django.contrib import messages

from .models import Message,Friend,Group,Good,Dm
from .forms import GroupCheckForm,GroupSelectForm,\
        SearchForm,FriendsForm,CreateGroupForm,PostForm,DMForm

from django.db.models import Q
from django.contrib.auth.decorators import login_required


# indexのビュー関数
@login_required(login_url='/admin/login/')
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

@login_required(login_url='/admin/login/')
def groups(request):
    # 自分が登録したFriendを取得
    friends = Friend.objects.filter(owner=request.user)
    
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
    
    # GETアクセス時の処理  
    else:
        # フォームの用意
        groupsform = GroupSelectForm(request.user)
        friendsform = FriendsForm(request.user, friends=friends, \
                vals=[])
        sel_group = '-'
    
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
@login_required(login_url='/admin/login/')
def add(request):
    # 追加するUserを取得
    add_name = request.GET['name']
    add_user = User.objects.filter(username=add_name).first()
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
@login_required(login_url='/admin/login/')
def creategroup(request):
    # Groupを作り、Userとtitleを設定して保存する
    gp = Group()
    gp.owner = request.user
    gp.title = request.POST['group_name']
    gp.save()
    messages.info(request, '新しいグループを作成しました。')
    return redirect(to='/sns/groups')

# メッセージのポスト処理
@login_required(login_url='/admin/login/')
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
        return redirect(to='/sns')
    
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
@login_required(login_url='/admin/login/')
def share(request, share_id):
    # シェアするMessageの取得
    share = Message.objects.get(id=share_id)
    print(share)
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
@login_required(login_url='/admin/login/')
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
@login_required(login_url='/admin/login/')
def mypage(request):
    params = {
         'name':request.user,
    }
    return render(request, "sns/mypage.html", params)

@login_required(login_url='/admin/login/')
def otherspage(request):
    #マイページを開きたいFriendの情報を取得
    fri_name = request.GET['name']
    fri_user = User.objects.filter(username=fri_name).first()
    params = {    
         'name':fri_user,
    }       
    return render(request, "sns/otherspage.html", params)

#DMのための処理
@login_required(login_url='/admin/login/')
def dm(request):
    #markはDMをおくるときにプルダウンから宛先を選ぶ場合を識別するためにdm.htmlに送る値
    mark = 0
    #DMでやりとりした内容を取得    
    dialogs = Dm.objects.filter(Q(owner=request.user) | Q(user=request.user))    
    #自分が追加したFriendの名前を選択できるようにformに入れる
    myfris = Friend.objects.filter(owner=request.user)
    #エラー回避のためにさきに定義しておく
    fri_name = ''

    #DMフォームを記入して送信するときの操作
    if request.method == "POST":
        obj = Dm()
        dms = DMForm(request.POST, instance=obj)
        dms.fields['user'].choices = [
            ("----", "----")
            ] + [
            (item.user, item.user) for item in myfris
            ]
        #DMの受け取り主を取得
        obj.owner = User.objects.filter(username=request.POST.get('user')).first()
        #DMの送り主を取得
        obj.user = User.objects.filter(username=request.user).first()
        
        if dms.is_valid():
           dms.save()
        form = DMForm()   
        form.fields['user'].choices = [
            ("----", "----")
            ] + [
            (item.user, item.user) for item in myfris
            ]
                            
    #Friendのマイページからとんできた場合
    elif request.GET['name'] != 'dst':#dstはdestination DMの宛先が未定のときと区別する
        #fri_nameにとんできた元のマイページ主の情報を取得
        fri_name = request.GET['name']
        form = DMForm()
        form.fields['user'].choices = [
            (fri_name, fri_name)
        ]
        obj = Dm()
        dms = DMForm(request.POST, instance=obj)
          
    else:           
        form = DMForm()    
        form.fields['user'].choices = [
            ("----", "----")
            ] + [
            (item.user, item.user) for item in myfris
            ]
        #mark=1のときはプルダウンでフレンドを選ぶとき    
        mark = 1
        obj = Dm()
        dms = DMForm(request.POST, instance=obj)        
    
    params = {
        "dialogs":dialogs,
        "dm_form":form,
        "mark": mark,
        "atesaki": fri_name,
    }
    return render(request, "sns/dm.html", params)

#通知ページを表示
@login_required(login_url='/admin/login/')
def notifications(request):
    params = {
        'note':request.user,
    }
    return render(request, "sns/notifications.html", params)

#自身の設定ページを表示
@login_required(login_url='/admin/login/')
def settings(request):
    params = {
          'name':request.user,
    }   
    return render(request, "sns/settings.html", params)

#グッドしたものの一覧を表示
@login_required(login_url='/admin/login/')
def goods(request):
    return(request, 'sns/goods.html')

#ブロックしたフレンドを表示
@login_required(login_url='/admin/login/')
def blocks(request):
    return('sns/blocks.html')       

#自分の登録しているフレンドを列挙するページ
@login_required(login_url='/admin/login/')
def all_friends(request):

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

            vlist = []  
            # FriendのUserをリストにまとめる
            for item in myfri:
                vlist.append(item.user.username)

            
            #フォームの用意
            groupsform = GroupSelectForm(request.user, request.POST)
      
    # GETアクセス時の処理  
    else:
        # フォームの用意
        groupsform = GroupSelectForm(request.user,request.POST)
        gp = Group.objects.all()
        myfri = Friend.objects.filter(owner=request.user)
        sel_group = '-'
    

    params = {
            'groups_form':groupsform,
            'group':gp,
            'friends':myfri,
            'gpname':sel_group,
        }

    return render(request, 'sns/all_friends.html', params)    


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
    public_group = Group.objects.filter \
            (owner=public_user).first()
    return (public_user, public_group)

    

# Create your views here.
