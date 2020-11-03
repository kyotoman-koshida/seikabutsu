# Short

低身長男性用マッチングアプリ

身長170cm未満の男性と身長不問の女性が交流できるように設計したウェブアプリケーションです。

# DEMO
https://kyotoman-app.herokuapp.com/　より「short」のページに進めます。
メールアドレスとパスワード、またはすでにtwitterを紐付けている場合にはtwitterでログインをすることができます。twitterを紐付けていない状態でログインをするとエラーになりますのでご注意ください。

![ログイン画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_login.png)


新規会員登録のボタンを押すと、以下の画面に遷移します。性別に「男性」を選び、なおかつ身長を170cm以上にして登録を行おうとすると「身長170cm以上の男性はご遠慮ください」と表示され、エラーとなります。（女性の身長は170cm以上であってもエラーになりません。）
![新規会員登録画面](https://github.com/kyotoman-koshida/image_files/blob/main/short_register.png)

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
![タイムライン](https://github.com/kyotoman-koshida/image_files/blob/main/short_timeline.png)


# Features

会員登録の必須入力項目に身長欄が設けられており、そこで男性は170cm未満に限定されます。普段は低い身長のゆえにハンデを負っている男性も、ここではそれを気にする必要はありません！

# Requirement
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

# Usage

DEMOの実行方法など、"hoge"の基本的な使い方を説明する

```bash
git clone https://github.com/hoge/~
cd examples
python demo.py
```

# Note
* 仮会員登録メールが届かないときは、迷惑メールフォルダーをご確認ください。
* ログイン画面のtwitter認証は一度メールアドレスでログインしたあとに、ログイン状態を維持してtwitterと紐付けることによって、次回以降ご利用いただけます。

# Author

* 越田達生（こしだたつお）
* 京都大学教育学部教育科学科現代教育基礎学系
* koshida.tatsuo.36w@st.kyoto-u.ac.jp

# License
copyright 2020 Tatsuo KOSHIDA.
