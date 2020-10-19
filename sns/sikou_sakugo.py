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
    myfris = Friend.objects.filter(owner=request.user
    #エラー回避のためにさきに定義しておく
    fri_name = ''                              

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

#form.pyの中にあるDMする相手をプルダウンで選ぶときに使うフォーム
class DMForm(forms.ModelForm):
    #選択肢の中からDMの送信先を決定
    user = forms.fields.ChoiceField(widget=forms.widgets.Select)
    class Meta:
        model = Dm
        fields = ['content']
        
#models.pyの中にあるDMモデル
class Dm(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_owner")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_user")
    content = models.CharField(max_length=250)
    dm_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner) + " が " + str(self.user) + " にDMしました " + \
            str(self.dm_at.month) + "/" + str(self.dm_at.day) + ")"

    class Meta:
        ordering = ["-dm_at"]
        

#templates/sns/dm.html
        {% extends 'sns/layout.html' %}

{% block title %}ダイレクトメッセージ{% endblock %}

{% block header %}
<h1>ダイレクトメッセージ</h1>

<form action="{% url 'dm' %}" method="post">
{% csrf_token %}
{% if mark == 1 %}
<input type="hidden" name="mode" value="__dm_form__">
{% else %}
<input type="hidden" name="mode" value={{atesaki}}>
{% endif %}
   {{dm_form}}
<button>送信</button>
</form>
<hr>
{% if dialogs %}
  {% for item in dialogs %}
  {{item}}
  {% endfor %}
{% else %}
DM履歴はありません
{% endif %}

{% endblock %}
