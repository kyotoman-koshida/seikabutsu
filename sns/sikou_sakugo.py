#実現したいこと：Friendクラスでマッチングアプリのユーザーのテーブルを作りたいです。ここでテーブルのフィールドの一つに身長を表すheightというフィールドがあるのですが、
#これに対するバリデーションとして、➀男性に限り　➁身長を150.0cmから169.9㎝に制限する。　を設けたいです。なお、性別は同じテーブルにあるgenderを参照したいです。
#➁だけなら問題なく実現できるのですが、➀はあの手この手を尽くしても今のところはうまくできていません。
#そもそも同じテーブルの他のフィールドを参照することができるのかも疑問に感じ始めています。
#以下私が試した四つのケースと、その行き詰まりを説明します。
#******************ここからは各ケースの共通部分************************
class Friend(models.Model):

    GENDER_CHOICES = (
         (1,'男性'),
         (2,'女性'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='friend_owner')
    user = models.ForeignKey(User, on_delete=models.CASCADE, \
            related_name='friend_user')
    gender = models.IntegerField(verbose_name='性別',choices=GENDER_CHOICES)     
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='グループ')
    place = models.CharField(max_length=100, verbose_name='居住地')
    introduce = models.CharField(max_length=250, verbose_name='自己紹介', null=True)

    #*************ここまでは各ケースに共通する部分***********************
#ケース１:自作バリデーションとしてsenbetu関数を作成した。これはgenderとheightを参照して、もしgender==1(これは男性を表す)ならheightを評価して、
#身長制限に引っかかったら（heightの値150.0未満、または170.0以上なら）raise ValidationErrorを引き起こす関数です。
#senbetu関数で➀と➁を実現させようと試みました。しかし、FloatFieldでvalidatorsリストにsenbetu関数を引数なしで（なぜ引数なしで試みたかというと、
#valueだけを引数として宣言したバリデーション用の関数はvalidatorsリストに引数なしで追加されるから、その模倣です)追加すると引数が足りなくエラーとなります。
#仕方がないので、valueとselfを引数とすると今度はvalueとselfが宣言されていないとされエラーとなります。
 　 def senbetu(value, self):
        if self.gender == 1:  #genderが1なら男性、2なら女性 
            if value<150.0 or value>169.9:
               raise ValidationError('身長は150.0cm以上、169.9cm以下でご記入下さい')            

    height =models.FloatField(validators=[senbetu(value, self)], verbose_name='身長')

    def __str__(self):
        GENDER = {1:'男性', 2:'女性',}   
        return str(self.user) + ' (性別:"' + GENDER[self.gender] + '")'


#ケース2:今度はケース１の失敗を踏まえ、senbetu関数の宣言をvalue変数のひとつだけで行うために、senbetu関数を➁のためだけに作成した。
#➀はif文を用いて実現させようと試みた。
#djangoの管理ツールを開いて、genderを男性と選択すれば「身長」項目が出現することを期待したが、管理ツールのSAVEボタンを押すとエラー（NOT NULL constraint failed）
    def senbetu(value):
        if value<150.0 or value>169.9:
            raise ValidationError('身長は150.0cm以上、169.9cm以下でご記入下さい')

    if gender == 1:        
       height =models.FloatField(validators=[senbetu], verbose_name='身長')

    def __str__(self):
        GENDER = {1:'男性', 2:'女性',}   
        return str(self.user) + ' (性別:"' + GENDER[self.gender] + '")'


#ケース3:heightのvalidatorsで➀と➁を実現させることは諦め、__str__関数で➀と➁の両方を行い、ページ遷移の際にエラーを引き起こそうと試みた。
#しかし、女性と身長制限を満たす男性にもエラー（自作したValidationError）が出現してしまう。
    height =models.FloatField(verbose_name='身長')

    def __str__(self):
        GENDER = {1:'男性', 2:'女性',}
        if self.gender == 1:
            if self.height < 150.0 or self.height > 169.9:
                raise ValidationError('170cm以上の男性は登録いただけません。')   
        return str(self.user) + ' (性別:"' + GENDER[self.gender] + '")'


#ケース4:FloatFieldの引数editableを使う方針に変更。
#senbetu関数で➁を実現させる。ただしこのバリデーションはeditable=Falseにすることで女性には適用されないことを目指した。
#新たにgencheck関数を作成し、これを用いてgender==2、つまり女性であればmen=Falseとなるようにした。
#FloatFieldの引数にeditable=menとおき、➀を実現させようとした。この場合エラーは発生しないが、なぜか女性でも身長の制限を受けてしまう。
    def senbetu(value):
        if value<150.0 or value>169.9:
            raise ValidationError('身長は150.0cm以上、169.9cm以下でご記入下さい')
    
    men = True
    def gencheck(self):
        if self.gender == 2:
           men = False

    height =models.FloatField(editable=men, validators=[senbetu], verbose_name='身長')
    
    def __str__(self):
        GENDER = {1:'男性', 2:'女性',}   
        return str(self.user) + ' (性別:"' + GENDER[self.gender] + '")'
