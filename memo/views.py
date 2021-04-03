from django.shortcuts import render
# from django.http import HttpResponse
# return HttpResponse("")
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.db.models import Count, TextField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .models import Question, Note
from .forms import NoteForm

# デバッグ用
import logging
logging.basicConfig(level=logging.DEBUG)
# logging.debug(a)


def index(request):
    # キーワード
    q = request.GET.get("q", "")
    # キーワードリスト
    qlist = []
    # キーワードがあれば
    if q != "":
        # 先頭と末尾の空白削除して、全角空白を半角にしてからリストに
        qlist = q.strip().replace("　", " ").split()

    queryset_q = []
    queryset_n = []

    # キーワードリストがあれば
    if len(qlist) > 0:
        # Question
        queryset_q = Question.objects.all()
        # Note
        queryset_n = Note.objects.all()

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

    # タグの重複削除方法がわからず set で対応
    # set オブジェクトに型変換
    queryset_q = set(queryset_q)
    queryset_n = set(queryset_n)

    context = {
        "title": "トップページ",
        "q": " ".join(qlist),
        "queryset_q": queryset_q,
        "queryset_n": queryset_n,
    }
    return render(request, "index.html", context)


def memo(request):
    # Paginator 用
    page = request.GET.get('page', 1)

    paginator = Paginator(Note.objects.all().order_by('-id'), 20)

    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages)

    context = {
        "title": "memo トップページ"
    }
    context["dataset"] = dataset
    return render(request, "memo/index.html", context)


def memo_detail(request, id):
    context = {
        "title": "memo 詳細ページ"
    }
    context["data"] = Note.objects.get(id=id)
    return render(request, "memo/detail.html", context)


def memo_create(request):
    """使わないけれども置いておく"""
    form = NoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = NoteForm()
    context = {
        'form': form
    }
    return render(request, "memo/create.html", context)


def qa(request):
    context = {
        "title": "質問ページ"
    }
    # カテゴリごとの投稿数の集計
    context["cate_agg"] = Question.objects.all().\
        values('cat', 'cat__name').\
        annotate(total=Count('cat')).\
        order_by('-total')

    return render(request, "qa/index.html", context)


def qa_start(request):
    clst = request.GET.getlist("c", None)

    if len(clst) > 0:
        logging.debug(clst)
        # 文字を数値に変える
        clst = [int(i) for i in clst]
        # IN句
        qs = Question.objects.filter(cat_id__in=clst)
    else:
        qs = Question.objects.all()

    # https://stackoverflow.com/questions/15874233/output-django-queryset-as-json
    data = list(qs.values('cat__name', 'answer', 'problem'))

    return JsonResponse(data, safe=False)


def qa_search(request):
    # Paginator 用
    page = request.GET.get('page', 1)
    # キーワード
    q = request.GET.get("q", "")
    # カラムを繋げておく
    queryset = Question.objects.annotate(
        hoge=Concat(
            'cat',
            Value(' '),
            'answer',
            Value(' '),
            'problem',
            output_field=TextField(),
        )
    )
    # 繋げたカラムを一つとして検索したものをPaginatorにする
    paginator = Paginator(queryset.filter(
        hoge__icontains=q).order_by('-id'), 100)

    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages)

    context = {
        "title": "質問リスト"
    }
    context["dataset"] = dataset

    return render(request, "qa/list.html", context)


def qa_detail(request, id):
    context = {
        "title": "質問詳細"
    }
    context["data"] = Question.objects.get(id=id)
    return render(request, "qa/detail.html", context)
