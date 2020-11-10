# マッチングアプリ「Short」

低身長男性用マッチングアプリ「short」の紹介。

身長170cm未満の男性と身長不問の女性が交流できるように設計したウェブアプリケーションです。
会員登録の必須入力項目に身長欄が設けられており、そこで男性は170cm未満に限定されます。普段は低い身長のゆえにハンデを負っている男性も、ここではそれを気にする必要はありません！
「short」の名前の由来は「背が低い」という意味の英単語です。

## こだわりポイント・工夫したポイント
* 身長にフィルターをかけるために、Djangoのカスタムユーザーを記述するdjango_app2/account/models.pyにて、身長のバリデーションを実装しました。
* DMに関して工夫したところに、DMを送る相手をあらかじめ指定しているかそうでないかで場合分けしました。具体的には、「DMを送る相手があらかじめ指定している場合」は他のユーザーのマイページから「DM」リンクを踏んでDMページに至った場合のことです。このとき、DMの送る相手はプルダウンメニューにあらかじめ指定されており変更ができなくなっています。また「DMを送る相手があらかじめ指定しているない場合」とは、ハンバーガーメニューの「DM」リンクからDMページへ直接とんだ場合のことです。このとき、DMを送る相手をプルダウンメニューから選ぶことができます。

## 問題点、改善点や発展させたい点
* デザイン面を後回しにして開発したため、CSSやJavaScriptの知識に乏しい。デザイン面にこれからの課題がある。
* 開発初期にアプリ名を安易に「sns」としてしまったため、ソースファイル上は「Short」ではなく「sns」のままとなってしまっている。この修正をするためにはソースファイルの「sns」を「Short」に置き換えたり、ローカル環境および本番環境のデータベースのテーブルの名前を変更しなければならないことに思い至り、時間の都合上なくなく断念。
* ユーザー情報にプロフィール画像や一言メッセージを追加したい。
* Twitterだけでなく、FacebookやInstgramのAPIも活用したい。
* 一度登録したフレンドやTwitterアカウント情報の削除ができるようにしたい。

## 簡単な機能の紹介
* 各ユーザーは他のユーザーを見つけて自分のフレンドに追加できる。
* 他のユーザーと自身の投稿などをタイムラインで共有できる。
* 他のユーザーとDMでやりとりすることができる。
* タイムラインに投稿されたメッセージに「share」(Twitterでいうところの「リツイート」に相当)や「good!」（Twitterでいうところの「いいね」に相当）をすることができる。
* 自分の登録したフレンドでグループを作ることができる。（LINEでの「グループライン」機能よりは音楽配信サービスなどの「プレイリスト」に近い）

## 具体的な使い方/チュートリアル
https://kyotoman-app.herokuapp.com/　より「short」のページに進めます。
メールアドレスとパスワード、またはすでにtwitterを紐付けている場合にはtwitterでログインをすることができます。twitterを紐付けていない状態でログインをするとエラーになりますのでご注意ください。

![ログイン画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_login.png)


まずは新規会員登録を行いましょう！新規会員登録ボタンを押してみます。
![新規会員登録画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_login2.png)

以下の画面に遷移するので、必要情報を入力してください。
![ユーザー情報登録](https://github.com/kyotoman-koshida/image_files/blob/main/short_register.png)

ここで、性別に「男性」を選び、かつ「身長」を170cm以上で入力すると以下のようなエラーが発生します。（女性の身長は不問です！）
![身長エラー](https://github.com/kyotoman-koshida/image_files/blob/main/short_validation.png)


「身長」を169cmに訂正し、その他必要情報を入力して登録をすると以下の画面に遷移して、仮登録が行われます。同時に登録したメールアドレスあてに本登録用のメールが送られます。メールが届かない場合は迷惑メールに振り分けられていないかご確認ください。
![仮登録画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_kari_regi.png)

本登録を行ったアカウントでログインすると、以下のようなトップページに移ります。このトップページには
* 紐付けたtwitterのtweetや、アプリ内で投稿したメッセージを表示するタイムライン
* 「トップページ」(index)、「グループ作成ページ」(group)、「マイページ」(mypage)、「登録しているフレンドの確認ページ」(check your friend)、「新しいフレンドを見つけるページ」(find new friend)、「DMページ」(DM)、「Twitterタイムラインページ」(Twitter timeline)へのリンクのあるメニューバー
* twitterアカウントを紐付けるボタン

![インデックス画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_index.png)

いまは新しく登録したばかりのユーザーを使っているので、まだフレンドがいません。新しくフレンドを探して追加しましょう！画面左側のピンク色のメニューバーをクリックしてください。（→）
![メニュー](https://github.com/kyotoman-koshida/image_files/blob/main/short_hamburger.png)

「find new friends」をクリックすると以下のような画面に遷移します。
![新しいフレンドを見つける](https://github.com/kyotoman-koshida/image_files/blob/main/short_alluser.png)

画面右側にある、新しくフレンドに加えたいユーザーの「add friend」をすると、自分のフレンドに登録されます！試しに何人か追加してみます。
![自分のフレンドにする](https://github.com/kyotoman-koshida/image_files/blob/main/short_addfriend.png)

さて、新しく追加したフレンドはデフォルトの「public」というグループに追加されます。しかし、自分で新しく他のグループを作ることもできます！さきほどのメニューバーから「group」をクリックすると以下のような画面に遷移します。新しくグループに加えたいユーザーにチェックをいれて、グループ名を入れれば新しいグループを作ることができます！
![グループ](https://github.com/kyotoman-koshida/image_files/blob/main/short_group.png)

試しにメニューバーの「check your friends」をクリックしてください。いま自分が追加しているフレンドの一覧が表示されます。
![全フレンド](https://github.com/kyotoman-koshida/image_files/blob/main/short_allfriend.png)

さらにグループを選択するプルダウンがあるので、そこで自分の選択したグループの全フレンドを参照できます。
![グループの全フレンド](https://github.com/kyotoman-koshida/image_files/blob/main/short_group_allfriend.png)

次にこの新しく作成したグループのタイムラインにメッセージを投稿をします！メニューバーから「post」をクリックしてください。投稿したメッセージをcontentに、投稿したいグループをgroupsのプルダウンから選びます！
![メッセージ投稿](https://github.com/kyotoman-koshida/image_files/blob/main/short_post.png)

投稿して、表示したいグループのタイムラインをチェックボックスにいれてupdateすると、新しく作ったグループのタイムラインに無事投稿できていることがわかります！
![メッセージ投稿完了](https://github.com/kyotoman-koshida/image_files/blob/main/short_post_done.png)

さて今度はpublicグループのタイムラインをみてみます。publicグループに投稿されているメッセージに対する「share」と「good!」機能について説明します。以下のメッセージを例にとります。現在「share」が１、「good!」が３となっています。これはそのまま一回shareされ、三回good!されたことを意味します。
![メッセージ](https://github.com/kyotoman-koshida/image_files/blob/main/short_message.png)

試しに「good!」を押してみると、「good!」が4に変化したことがわかります。
![グッド](https://github.com/kyotoman-koshida/image_files/blob/main/short_message_good.png)

それでは次に「share」を押してみましょう。以下のような画面になるはずです。
![シェア](https://github.com/kyotoman-koshida/image_files/blob/main/short_share.png)

この「share」をしたいグループに投稿すると以下のようになります。
![シェア完了](https://github.com/kyotoman-koshida/image_files/blob/main/short_share_done.png)

次にDM機能について紹介します。メニューバーから「DM」を選択してみてください。
![DM](https://github.com/kyotoman-koshida/image_files/blob/main/short_dm.png)

contentにDMの内容、userにDMをしたい相手を選ぶことで以下の様にDMができます！
![DM完了](https://github.com/kyotoman-koshida/image_files/blob/main/short_dm_done.png)

ちなみにDMはユーザーページからもすることができます。さきほどの「check your friends」をみてください。名前のよこに「マイページ」というリンクがあります。
![全フレンド](https://github.com/kyotoman-koshida/image_files/blob/main/short_allfriend.png)

このリンクからフレンドのマイページに移ることができます。
![フレンドのマイページ](https://github.com/kyotoman-koshida/image_files/blob/main/short_otherspage.png)

画面右側にある「DMする」のリンクからDMページに移ることができます。なおこのようにしてDMページに移った時には、DMの宛先のuserプルダウンメニューにあらかじめ遷移もとのユーザーの名前が入力されています。
![DMのあてさき](https://github.com/kyotoman-koshida/image_files/blob/main/short_dm_atesaki.png)

メニューバーから「find new friends」をクリックしても同様にしてDMをすることができますが、この場合はフレンド登録していないユーザーにもDMをすることができます。また、自分自身のマイページを確認することもできます。メニューバーの「mypage」をクリックすると、以下のページに遷移します。
![自分のマイページ](https://github.com/kyotoman-koshida/image_files/blob/main/short_mypage.png)

さて、最後のTwitterとの紐付けについてみていきます。トップページ画面上方にある「Twitterを紐付け」ボタンをクリックしてください。以下のような画面になるので、紐付けたいTwitterアカウントのユーザー名とパスワードを入力してひもつけます。
![Twitter認証](https://github.com/kyotoman-koshida/image_files/blob/main/short_twitter_ninsho.png)

Twitterの紐付けを行うと、メニューバーの「Twitter timeline」から紐付けたTwitterの最近のタイムライン（２０件まで）を確認できます。このうちの好きなツイートをこの「Short」上の好きなグループのタイムラインに反映されることができます！
![ツイッタータイムライン](https://github.com/kyotoman-koshida/image_files/blob/main/short_twitter_timeline.png)

一度ツイッターを紐付ければ、次のログインからは「Twitterログイン」ボタンでログインすることができます。
![ツイッターログイン](https://github.com/kyotoman-koshida/image_files/blob/main/short_login2.png)


## 改善点・発展させたい点
* マイページにプロフィール画像やひとこと紹介を表示させたい。
* 検索機能を充実させたい。居住地や身長などでも検索できるようにしたい。
* Twitterだけでなく、他のSNSのAPIも利用したい。
* CSSやJavaScriptの理解を深めて、もっとデザインや操作性を向上させたい。
* ユーザーをブロックしたり、ブロックを解除させたりできるようにしたい。
* グループやフレンドなど一度登録したものの削除をユーザーが自由に行えるようにしたい。

## Requirement
* asgiref==3.2.10
* astroid==2.4.2
* certifi==2020.6.20
* cffi==1.14.3
* chardet==3.0.4
* colorama==0.4.3
* cryptography==3.1.1
* defusedxml==0.7.0rc1
* dj-database-url==0.5.0
* dj-static==0.0.6
* Django==3.1.1
* django-heroku==0.3.1
* django-toolbelt==0.0.1
* django-utils-six==2.0
* gunicorn==20.0.4
* idna==2.10
* isort==5.5.2
* lazy-object-proxy==1.4.3
* mccabe==0.6.1
* oauthlib==3.1.0
* pycparser==2.20
* PyJWT==1.7.1
* pylint==2.6.0
* python3-openid==3.2.0
* pytz==2020.1
* requests==2.24.0
* requests-oauthlib==1.3.0
* six==1.15.0
* social-auth-app-django==4.0.0
* social-auth-core==3.3.3
* sqlparse==0.3.1
* static3==0.7.0
* toml==0.10.1
* twitter==1.18.0
* urllib3==1.25.10
* whitenoise==3.3.1
* wrapt==1.12.1
* psycopg2==2.8.6

## テストユーザー

* 男性版テストユーザー email:taro@yamada.com, pass:yamadataro
* 女性版テストユーザー email:hanako@ueda.com, pass:uedahanako

## 注意点
* 仮会員登録メールが届かないときは、迷惑メールフォルダーをご確認ください。
* ログイン画面のtwitter認証は一度メールアドレスでログインしたあとに、ログイン状態を維持してtwitterと紐付けることによって、次回以降ご利用いただけます。

## 著者

* 越田達生（こしだたつお）
* 京都大学教育学部教育科学科現代教育基礎学系
* koshida.tatsuo.36w@st.kyoto-u.ac.jp

### License
copyright 2020 Tatsuo KOSHIDA.
