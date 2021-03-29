import os
import sqlite3
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qa.settings")

import django  # noqa
django.setup()

# ↓ django.setup()の後にする
from memo.models import Question, Category  # noqa


# 既存の sqlite データベース　manage.py と同階層に置く
dbname = 'qa.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# カテゴリインポートを先に行う
cur.execute('SELECT DISTINCT category FROM qa')
cate = cur.fetchall()
for v in cate:
    obj = Category(name=v[0])
    obj.save()


# Question インポートはカテゴリが出来た後に行う
cur.execute('SELECT * FROM qa')
rows = cur.fetchall()
for _, c, a, q in rows:
    # カテゴリの検索してオブジェクトを得る
    c_obj = Category.objects.get(name=c)
    # Question オブジェクト作成
    q_obj = Question()
    q_obj.cat = c_obj
    q_obj.answer = a
    q_obj.problem = q
    q_obj.save()


conn.close()


# Category 表示例
# for q in Category.objects.all():
#     print(q.name)

print("インポート終了")
