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



以上
