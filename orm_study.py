import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qa.settings")
import django  # noqa

from django.db.models import Q, Value
from django.db.models import Count, TextField
from django.db.models.functions import Concat

django.setup()


# ※注意　モデルのインポートは ↓ django.setup()の後にする
# この自作モデルの詳細は memo/models.py を参照
from study1.models import Book, Review  # noqa
from memo.models import Question, Category, Note, Tag  # noqa

#
# Django ORMの勉強
#

# クエリセット -> モデルのオブジェクトのリスト
"""
クエリセットはいつ評価されるのか

内部的には、クエリセットの生成、フィルタ操作、スライス、コード間の受渡しは、 データベースを操作することなく行えます。
クエリセットを何らかの形で評価しな い限り、データベースの操作は実際には起こらないのです。

以下の方法を使うと、クエリセットを評価できます:

イテレーション
クエリセットはイテレーション可能オブジェクトであり、
オブジェクトに対して最初にイテレーション操作を行ったときにデータ ベースクエリを実行します。
例えば、以下の例はデータベース中の全てのエ ントリのヘッドラインを出力します:

for e in Entry.objects.all():
    print e.headline


スライス
クエリセットに制約を課すで説明しているように、 Python の配列スライス表記を使うとクエリセットをスライスできます。
通常、 クエリセットに対するスライスは (未評価の) 別のクエリセットを返します が、
スライス表記に「ステップ (step)」パラメタを使った場合には、データ ベースクエリを実行します。

repr(). クエリセットに対して repr() を呼び出すと、クエリセッ トは値評価されます。
これは Python 対話インタプリタでの利便性のための 仕様で、API を対話的に使うときに結果を即座に見られるようにしています。

len(). クエリセットに対して len() を呼び出すと、クエリセッ トは値評価されます。
予想に違わず、 len() はクエリ結果リストの長さを返します。

注意: クエリセット中のレコードの数を知りたいだけなら、 len() は 使わないでください 。
レコード数の計算はデータベース上で SQL 文の SELECT COUNT(*) 使って行う方が遥かに効率的であり、
まさにその理由 から Django では count() メソッドを提供しています。後述の count() を参照してください。

list(). クエリセットに対して list() を呼び出すと、値評価を強 制できます。例えば:

entry_list = list(Entry.objects.all())

とはいえ、この方法を使うと、Django が全ての要素のリストをメモリ上にロー ドするため、
巨大なメモリオーバヘッドを引き起こす可能性があるので十分 注意してください。
これに対し、クエリセットに対するイテレーション操作 では、
必要な分だけデータをロードしてオブジェクトをインスタンス化する という利点があります。


検索

#フィールド名__演算子=比較値
#アンダースコア２つでつなぐ。スペースは入れない。
Person.objects.filter(name__startwith='T')

#演算子未指定時は完全一致（exact）として扱われる
Person.objects.filter(name='Taro')

#カンマで区切ることで、複数の条件を指定可能（ANDになる）
Entry.objects.filter(name='Taro', age__gte=12)

#条件はQオブジェクトでも指定可能。
#OR条件の指定はQオブジェクトを使わなければできない。
from django.db.models import Q
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)

#条件にフィールド値を使う場合はFオブジェクトを使う
from django.db.models import F
# Find companies that have more employees than chairs.
Company.objects.filter(num_employees__gt=F('num_chairs'))

#そのまま計算にも使える
reporter.update(stories_filed=F('stories_filed') + 1)


キーワード 	効果
exact, iexact 	完全一致 ※演算子未指定時のデフォルト
contains, icontains 	部分一致
in 	いずれかを完全一致（配列を指定）
gt 	超
gte 	以上
lt 	未満
lte 	以下
startswith, istartswith 	～で始まる
endswith, iendswith 	～で終わる
range 	範囲指定
regex, iregex 	正規表現
isnull 	null判定
date,year...second 	時間の要素で判定（以下参照）

小文字のiがついているのは大文字小文字の区別無しバージョン


null判定はisnull以外のもfilter(pub_date=None)でもできる。
isnullは主にIS NOT NULLの指定で使う。

filter(pub_date__isnll=False)

時間系のキーワードはdateまたはdatetimeフィールドに続けて指定し、
任意の要素（年、月、日、時間など）を取り出して比較する際に使う

filter(pub_date__year__gt>2017)

データベース関数

update, create, filter, order by, annotation, aggregate の各メソッドではデータベース関数を使うことができる。

#例 LENGTH関数 名前の長さで昇順に並び替え
Company.objects.order_by(Length('name').asc())


"""


def test1():
    # クエリセットからインスタンスを取得する 	検索に一致したもの 	get(**kwargs)
    print(Category.objects.get(pk=2).query)
    c = Category.objects.get(pk=2)
    # SELECT "memo_category"."id", "memo_category"."name" FROM "memo_category" WHERE "memo_category"."id" = 2 LIMIT 21;
    print(c)
    print(c.id)
    print(c.name)


def test2():
    print(Question.objects.all()[5:10].query)
    # SELECT "memo_question"."id", "memo_question"."cat_id", "memo_question"."answer", "memo_question"."problem" FROM "memo_question" LIMIT 5 OFFSET 5
    all = Question.objects.all()[5:10]
    print(all)


def test3():
    q1 = Question.objects.all()
    all = q1.filter(cat__name='Python').order_by('id').reverse()[:2]
    print(all)

    print(q1.filter(cat__name='Python').order_by('id').reverse()[:2].query)
    # SELECT "memo_question"."id", "memo_question"."cat_id", "memo_question"."answer", "memo_question"."problem" FROM "memo_question" INNER JOIN "memo_category" ON ("memo_question"."cat_id" = "memo_category"."id") WHERE "memo_category"."name" = Python ORDER BY "memo_question"."id" DESC LIMIT 2


def test4():
    # 新規作成
    # get_or_createメソッドメソッドのように該当データがあれば取得、なければ新規作成して取得という複合的なメソッドもある
    c = Category()
    c.name = "Bash"
    c.save()


def test5():
    # 更新
    # b = Blog.objects.get(id=1)
    # b.name = 'new Name'
    # b.save() #ここでUPDATEが実行される

    c = Category.objects.filter(name="Bash")
    print(c)
    # <QuerySet [<Category: Bash>]>

    # これはクエリセットの先頭のオブジェクトを返す
    c = Category.objects.filter(name="Bash").first()
    print(c)

    c.name = "Bash2"
    c.save()


def test6():
    # 削除
    # b = Blog.objects.get(id=1)
    # b.delete() #DELETEが実行される
    c = Category.objects.filter(name="Bash").first()
    print(c)  # Bash2 に変更しているので None

    c = Category.objects.filter(name="Bash2").first()
    print(c.id)  # 10

    # 利便性のために、 Django には pk という照合形式があります。 pk は primary_key を表します
    obj = Category.objects.get(pk=10)
    print(obj)
    obj.delete()


def test7():
    from django.db.models.functions import Length

    # 文字の長さの降順
    a = Category.objects.order_by(Length('name').desc())
    print(a)


def test8():
    # Question から Category を引く場合は select_related を使ってあげれば
    # ループの度に Category を select せずに join してまとめて取ってきてくれる。
    for v in Question.objects.all().select_related():
        print(v.cat)

    print("-" * 50)

    # Category から Question の一覧を引っ張る場合は prefetch_related を使うと良い
    for v in Category.objects.all().prefetch_related("question_set"):
        print(v)


def test9():
    # SELECT "memo_category"."id", "memo_category"."name" FROM "memo_category" INNER JOIN "memo_question" ON ("memo_category"."id" = "memo_question"."cat_id") WHERE "memo_question"."answer" = columns
    print(Category.objects.filter(question__answer="columns").query)
    o = Category.objects.filter(question__answer="columns")
    print(len(o))
    print(o)


def test10():
    # Django ORMには<Model>.objects.values()と<Model>.objects.only()という
    # values()とonly()という似たようなメソッドがある
    # 迷いたくないなら only を使え
    # values()が返すのはQuerySetではなくValuesQuerySet
    # only()を使うとQuerySetが返ってくる

    print(Question.objects.filter(answer="columns").query)
    # SELECT "memo_question"."id", "memo_question"."cat_id", "memo_question"."answer", "memo_question"."problem" FROM "memo_question" WHERE "memo_question"."answer" = columns
    print(Question.objects.filter(answer="columns").only("answer").query)
    # SELECT "memo_question"."id", "memo_question"."answer" FROM "memo_question" WHERE "memo_question"."answer" = columns
    o = Question.objects.filter(answer="columns").only("answer")
    # コラムのanswerを指定しているが
    # problemにアクセスすると、エラーになるではなく、再度完全なオブジェクトのqueryが走って再取得した結果を利用する
    print(o[0].problem)


def test11():
    # len()は負荷がかかるのでつかわない
    a = Book.objects.count()
    b = Review.objects.count()
    print(a)
    print(b)

    # targetのnameが、よくわかるPythonの本
    a = Review.objects.filter(target__title='本1').count()
    print(a)

    # 価格が2000以上。gteはgreater than equal の略
    b = Book.objects.filter(price__gte=2000).count()
    print(b)

    # 全ての書籍の集計 aggregate
    from django.db.models import Avg, Max, Min
    a = Book.objects.aggregate(Avg('price'))
    print(a)
    b = Book.objects.aggregate(Max('price'), Min('price'), Avg('price'))
    print(b)


def test12():
    # annotate()は、QuerySet の各アイテムに対する集計を生成します。
    # ForeignKeyやManyToManyField等、他のモデルと何らかの関係で紐づいていて、
    # それらに関する集計に使うことになります。
    from django.db.models import Count
    a = Book.objects.annotate(Count('review'))
    for v in a:
        print(f'書籍名:{v.title} - レビュー数:{v.review__count}')

    # キーワード引数名として指定すると、その名前で格納されます
    for book in Book.objects.annotate(reviews=Count('review')):
        print('書籍名:{} - 評価数:{}'.format(book.title, book.reviews))

    # 紐づいたレビューのうち、一番高い評価も取得します。
    from django.db.models import Avg, Max, Min

    for book in Book.objects.annotate(max_review=Max('review__point')):
        print('書籍名:{} - 最高評価:{}'.format(book.title, book.max_review))

    # レビュー数の多い本から表示するようにしてみましょう。
    for book in Book.objects.annotate(reviews=Count('review')).order_by('-reviews'):
        print('書籍名:{} - 評価数:{}'.format(book.title, book.reviews))


def test13():
    # 文字列カラムを繋げて一度に検索
    from django.db.models import Value, TextField
    from django.db.models.functions import Concat

    queryset = Note.objects.annotate(
        search_name=Concat(
            'cat__name', Value(' '),
            'tags__name', Value(' '),
            'title', Value(' '),
            'content', output_field=TextField()
        )
    )

    # then you can filter:
    a = queryset.filter(search_name__icontains='機械学習')

    print(a)


def test14():
    # 逆参照 note_set
    o = Tag.objects.filter(note__title__contains="from")
    for v in o:
        print(v.note_set.all())


def test15():
    # 複数テーブル横断検索

    # キーワード
    q = "　import  channel"
    # キーワードリスト
    qlist = []
    # キーワードがあれば
    if q != "":
        # 先頭と末尾の空白削除して、全角空白を半角にしてからリストに
        qlist = q.strip().replace("　", " ").split()

    # Question
    queryset_q = Question.objects.all()
    # Note
    queryset_n = Note.objects.all()
    # キーワードリストがあれば
    if len(qlist) > 0:
        # Q オブジェクトを
        q_object = Q()
        # キーワード分
        for v in qlist:
            # and でつなげる
            q_object.add(Q(search__icontains=v), Q.AND)

        # add したものはキーワードにより例えばこうなっている
        # (AND: ('search__icontains', 'import'), ('search__icontains', 'select'), ('search__icontains', 'app'), ('search__icontains', 'numpy'))

        # annotate Concat を使用して、カラムをつなげ
        # 最後の filter に上で作成した q_object を挿入

        # Question 用
        queryset_q = queryset_q.\
            annotate(
                search=Concat(
                    'cat',
                    Value(' '),
                    'tags__name',
                    Value(' '),
                    'answer',
                    Value(' '),
                    'problem',
                    output_field=TextField(),
                )
            ).filter(q_object)

        # Note 用
        queryset_n = queryset_n.\
            annotate(
                search=Concat(
                    'cat',
                    Value(' '),
                    'tags__name',
                    Value(' '),
                    'title',
                    Value(' '),
                    'content',
                    output_field=TextField(),
                )
            ).filter(q_object)

    print(queryset_q)
    print(queryset_n)





if __name__ == "__main__":
    test15()
