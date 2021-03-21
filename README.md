# Django アプリ


## 初期設定

```
python -m django --version
3.1.7
```

- githubでリポジトリ作成(qaにした)
- パソコンのどこかの場所で
```
git clone https://github.com/kawain/qa.git
```
- qaフォルダができる
- qaフォルダ内で(※最後のドットが重要)
```
django-admin startproject qa .
```
- `settings.py` の日本語日本時間設定
```
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
```
- `gitignore` を作成
```
*__pycache__
*.sqlite3
```
- データベース作成(Djangoで用意している11個のテーブルができる)
```
python manage.py migrate
```
- スーパーユーザー作成
```
python manage.py createsuperuser
```
- 開発用サーバー起動
```
python manage.py runserver
```
http://127.0.0.1:8000/  
スーパーユーザーでログイン  
http://127.0.0.1:8000/admin/  


## アプリケーション作成

- memo という名
```
python manage.py startapp memo
```
- テストのビュー作成  memo/views.py
```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world.")

```
- qa/urls.py urlが少ないのが見込まれるのでファイルを分けない
```
from django.contrib import admin
from django.urls import path
from memo import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
]
```
- 開発用サーバー起動確認

## モデル作成

- settings.py の INSTALLED_APPS にアプリを追加しから

```
python manage.py makemigrations <app name>

python manage.py migrate
```
- 実行例
```

$ python manage.py makemigrations memo
Migrations for 'memo':
  memo\migrations\0001_initial.py
    - Create model Category
    - Create model Tag
    - Create model Question
    - Create model Note

$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, memo, sessions
Running migrations:
  Applying memo.0001_initial... OK
```

- admin.py に登録

## Django のモデルにデータインポート

- data_import.py
 ローカルのスクリプトから Django の環境を呼んでモデルの操作する



以上
