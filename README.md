# Short

低身長男性用マッチングアプリ「short」の紹介。

身長170cm未満の男性と身長不問の女性が交流できるように設計したウェブアプリケーションです。
会員登録の必須入力項目に身長欄が設けられており、そこで男性は170cm未満に限定されます。普段は低い身長のゆえにハンデを負っている男性も、ここではそれを気にする必要はありません！

# こだわりポイント・みてほしいポイント
* 身長にフィルターをかけるために、Djangoのカスタムユーザーを記述するdjango_app2/account/models.pyにて、身長のバリデーションを実装しました。
* DMに関して工夫したところに、DMを送る相手をあらかじめ指定しているかそうでないかで場合分けしました。具体的には、「DMを送る相手があらかじめ指定している場合」は他のユーザーのマイページから「DM」リンクを踏んでDMページに至った場合のことです。このとき、DMの送る相手はプルダウンメニューにあらかじめ指定されており変更ができなくなっています。また「DMを送る相手があらかじめ指定しているない場合」とは、ハンバーガーメニューの「DM」リンクからDMページへ直接とんだ場合のことです。このとき、DMを送る相手をプルダウンメニューから選ぶことができます。


## 使い方
https://kyotoman-app.herokuapp.com/　より「short」のページに進めます。
メールアドレスとパスワード、またはすでにtwitterを紐付けている場合にはtwitterでログインをすることができます。twitterを紐付けていない状態でログインをするとエラーになりますのでご注意ください。

![ログイン画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_login.png)


まずは新規会員登録を行いましょう！新規会員登録ボタンを押してみます。
![新規会員登録画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_login2.png)

以下の画面に遷移するので、必要情報を入力してください。
![ユーザー情報登録](https://github.com/kyotoman-koshida/image_files/blob/main/short_register.png)

ここで、性別に「男性」を選び、かつ「身長」を170cm以上で入力すると以下のようなエラーが発生します。
![身長エラー](https://github.com/kyotoman-koshida/image_files/blob/main/short_validation.png)


必要情報を入力して登録をすると以下の画面に遷移して、仮登録が行われます。同時に登録したメールアドレスあてに本登録用のメールが送られます。メールが届かない場合は迷惑メールに振り分けられていないかご確認ください。
![仮登録画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_kari_regi.png)

本登録を行ったアカウントでログインすると、以下のようなトップページに移ります。このトップページには
* 紐付けたtwitterのtweetや、アプリ内で投稿したメッセージを表示するタイムライン
* マイページへのリンク
* タイムラインに投稿するためのページへのリンク
*　自分が登録しているフレンドへダイレクトメッセージ（以下DM）を送るためのページへのリンク
* 自分の登録しているフレンドを管理しやすくするためのグループ作成ページへのリンク
* 自分の登録している全てのフレンドを確認するページへのリンク
* twitterアカウントを紐付けるボタン
* twitterが紐付けられている場合に最近のtwitterタイムラインを反映させるページへのリンクが含まれています。(紐付けられていない場合にはエラーとなります。)

![インデックス画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_index.png)

タイムラインについて詳しく見ていきます。
タイムラインには先述のとおり、紐付けたtwitterのtweetやアプリ内で投稿したメッセージが表示されます。デフォルトでは、「public」という名前のグループが表示されています。
![タイムライン](https://github.com/kyotoman-koshida/image_files/blob/main/short_timeline.png)

次にタイムライン上のメッセージについて、「good」「shre」「add friend」機能について紹介します。
以下のメッセージについてみることにします。
![メッセージ](https://github.com/kyotoman-koshida/image_files/blob/main/short_message.png)

* まず「share」機能についてみます。
このメッセージを「test_group」にshareします。shareの時には自分のコメントを付加できます。
![メッセージシェア](https://github.com/kyotoman-koshida/image_files/blob/main/short_share.png)
「share!」のボタンを押すと以下のようにタイムラインに新たに表示されます。
![メッセージシェア２](https://github.com/kyotoman-koshida/image_files/blob/main/short_share_done.png)
タイムラインの上にはグループのチェックボックスがあります。自分の好きなグループを選択してupdateボタンを押すと、そのグループのタイムラインを表示します。例えば、ここで自分で作成した「test_group」という名前のグループを選択すると以下のように、「test_group」のタイムラインが表示されます。
![タイムライン２](https://github.com/kyotoman-koshida/image_files/blob/main/short_timeline2.png)

*このメッセージで「good」機能を使ってみます。「good」ボタンを押すとgoodカウントが0から1になります。
![メッセージグッド](https://github.com/kyotoman-koshida/image_files/blob/main/short_good_done.png)


さて今度はタイムラインへの投稿についてみていきます。画面左上のハンバーガーメニューをクリックしてください。
「index」「post」「group」「mypage」「DM」の項目があります。「index」を押すとはトップページへ戻ります。
![メニュー](https://github.com/kyotoman-koshida/image_files/blob/main/short_hamburger.png)

*「post」機能について。タイムラインへ投稿をしてみます。「post」のリンクをクリックしてみて下さい。すると以下のような画面になります。今回はメッセージを「test_group2」へ投稿します。
![投稿](https://github.com/kyotoman-koshida/image_files/blob/main/short_post.png)

タイムライン上のチェックボックスで「test_group2」にチェックをいれてupdateすると今投稿したメッセージがあるのがわかります。
![投稿完了](https://github.com/kyotoman-koshida/image_files/blob/main/short_post_done.png)

*「group」機能について。新しくグループを作成してみます。「group」のリンクをクリックしてみて下さい。自分が登録している好きなフレンドをグループに加えて新しいグループを作成することができます。ここでは上から五人を「test_group3」に加えて作成しています。
![グループ作成](https://github.com/kyotoman-koshida/image_files/blob/main/short_group.png)

ユーザーを探して新しくフレンドに加えることもできます。上の画像に「新しいフレンドを見つける」というリンクがあるので、それをクリックしてみて下さい。すべての（異性の）ユーザーが表示されます。
![全ユーザー](https://github.com/kyotoman-koshida/image_files/blob/main/short_alluser.png)
ここで各レコードの隣にある「add friend」を押すと新しくフレンドに登録することができます。

自分の登録しているフレンドの一覧をみることもできます。全ユーザー一覧でも、全フレンド一覧でもユーザー検索をすることができます。
![全フレンド](https://github.com/kyotoman-koshida/image_files/blob/main/short_allfriend.png)

実際に登録しているフレンドのうち「まり」さんを検索すると、「該当するユーザー」に表示されて以下のようになる。
![ユーザー検索](https://github.com/kyotoman-koshida/image_files/blob/main/short_allfriend_search.png)

またグループごとにフレンドを表示したい場合は、プルダウンメニューから目的のグループ名をいれて「Select Group」を押すことで表示させることができます。
![ユーザーグループ表示](https://github.com/kyotoman-koshida/image_files/blob/main/short_friend_group.png)

フレンド名横にあるリンクから、各フレンドのマイページへとぶこともできます。実際にとぶと以下のようなマイページをみることができます。
![他人のマイページ](https://github.com/kyotoman-koshida/image_files/blob/main/short_otherspage.png)

*「マイページ」について。もちろん自分自身のマイページをみることもできます。先ほどのメニューから「mypage」をクリックしてみると、以下のようなマイページをみることができます。
![マイページ](https://github.com/kyotoman-koshida/image_files/blob/main/short_mypage.png)

*「DM」について。自分のフレンド登録をしているユーザーとやり取りをすることができます。
![ダイレクトメッセージ](https://github.com/kyotoman-koshida/image_files/blob/main/short_dm.png)

Twitterとの紐付けについて。トップページ（index）の上方に「Twitterと紐付け」のボタンがあります。それをクリックすると、以下のようなページとなり認証を求められます。ユーザー名とパスワードを入力することでログインすることができます。
![ツイッター認証](https://github.com/kyotoman-koshida/image_files/blob/main/short_twitter_ninsho.png)

一度ツイッターを紐付ければ、次のログインからはTwitterでログインすることができます。また、自身のTwitterタイムライン上のTweetをこのアプリのタイムラインへ反映させることができます。


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
