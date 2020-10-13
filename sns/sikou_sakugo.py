#マッチングアプリでDMを送るための関数を作りたいのですが、そのDMをデータベースに保存することができません。
#DMを送るパターンは二種類想定していて、一つはフレンド一覧からDMを送る相手を先に決めてからDMをする場合と、
#もう一つは先にDMページに行って、プルダウンメニューでDMを送る相手を決めてDMを送る場合です。
#いずれの場合もdm関数内のdms.save()で引っかかり、"The Dm could not be created because the data didn't validate."となってエラーとなってしまいます。
#エラー文を読むと、バリデーションされていないからエラーが起きたことが分かりますが、何をどうバリデートするのかが分かりません。


#views.py下にある該当のdm関数のコード
#DMのための処理
@login_required(login_url='/admin/login/')
def dm(request):
    #markはDMをおくるときにプルダウンから宛先を選ぶ場合を識別するためにdm.htmlに送る値
    mark = 0
    #DMでやりとりした内容を取得    
    dialogs = Dm.objects.filter(owner=request.user)    
    #自分が追加したFriendの名前を選択できるようにformに入れる
    myfri = Friend.objects.filter(owner=request.user)

    #DMフォームを記入して送信するときの操作
    if request.method == "POST":
        obj = Dm()
        dms = DMForm(request.POST, instance=obj)
        dms.save()        

    #Friendのマイページからとんできた場合
    elif request.GET['name'] != 'dst':#dstはdestination DMの宛先が未定のときと区別する
        #fri_nameにとんできた元のマイページ主の情報を取得
        fri_name = request.GET['name']
        form = DMForm()
        form.fields['user'].choices = [
            (fri_name, fri_name)
        ]
    #DMページからとんできた場合    
    else:           
        form = DMForm()    
        form.fields['user'].choices = [
            ("----", "----")
            ] + [
            (item.user, item.user) for item in myfri
            ]
        #mark=1のときはプルダウンでフレンドを選ぶとき    
        mark = 1       
    
    params = {
        "dialogs":dialogs,
        "dm_form":form,
        "name":myfri,
        "mark": mark,
        "atesaki": fri_name,
        
    }
    return render(request, "sns/dm.html", params)

#form.pyの中にあるDMする相手をプルダウンで選ぶときに使うフォーム
class DMForm(forms.ModelForm):
    #選択肢の中からDMの送信先を決定
    user = forms.fields.ChoiceField(widget=forms.widgets.Select)
    class Meta:
        model = Dm
        fields = ['content']
