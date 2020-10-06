#実現したいこと：➀男性に限り
#　　　　　　　　➁身長を150.0cmから169.9㎝に制限する。
#以上➀と➁を一つのテーブル内でのバリデーションとしたい。
#クラス内の要素の実現値をクラス内の関数で参照するうえでのことが問題の本質になっていると思います。
#各ケースを実行したうえでエラー対応などもしましたが、解決には至っていません。

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
#ケース１:senbetu関数で➀と➁を実現させようと試みた。しかし、heightでvalidatorsリストに加えたsenbetu関数の引数の問題でエラーが出現。
 　 def senbetu(value, self):
        if self.gender == 1:  #genderが1なら男性、2なら女性 
            if value<150.0 or value>169.9:
               raise ValidationError('身長は150.0cm以上、169.9cm以下でご記入下さい')            

    height =models.FloatField(validators=[senbetu(value, self)], verbose_name='身長')

    def __str__(self):
        GENDER = {1:'男性', 2:'女性',}   
        return str(self.user) + ' (性別:"' + GENDER[self.gender] + '")'


#ケース2:senbetu関数で➁を、if文で➀を実現させようと試みた。管理画面で男性を選択すれば「身長」項目が出現することを期待したが、その他の項目を記入しSAVEボタンを押すとエラー
    def senbetu(value):
        if value<150.0 or value>169.9:
            raise ValidationError('身長は150.0cm以上、169.9cm以下でご記入下さい')

    if gender == 1:        
       height =models.FloatField(validators=[senbetu], verbose_name='身長')

    def __str__(self):
        GENDER = {1:'男性', 2:'女性',}   
        return str(self.user) + ' (性別:"' + GENDER[self.gender] + '")'


#ケース3:heightのvalidatorsで➀と➁の実現は諦め、__str__関数でページ遷移の際にエラーを引き起こそうと試みた。しかし、女性でも身長制限を満たす男性にもエラーが出現してしまう。
    height =models.FloatField(verbose_name='身長')

    def __str__(self):
        GENDER = {1:'男性', 2:'女性',}
        if self.gender == 1:
            if self.height < 150.0 or self.height > 169.9:
                raise ValidationError('170cm以上の男性は登録いただけません。')   
        return str(self.user) + ' (性別:"' + GENDER[self.gender] + '")'


#ケース4:senbetu関数で➁を、モデルフィールドの引数editableで➀を実現させようと試みた。エラーは発生しないが、女性でも身長の制限を受けてしまう。
    def senbetu(value):
        if value<150.0 or value>169.9:
            raise ValidationError('身長は150.0cm以上、169.9cm以下でご記入下さい')
    
    men = True
    def gencheck(self):
        if self.gender == 2:
           men = False

    height =models.FloatField(editable=men, validators=[senbetu], verbose_name='身長')