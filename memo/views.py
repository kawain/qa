from django.shortcuts import render

# from django.http import HttpResponse
# return HttpResponse("")
from django.db.models import Value
from django.db.models.functions import Concat
from django.db.models import Count, TextField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.http import JsonResponse
from .models import Category, Tag, Question, Note
from .forms import NoteForm

# デバッグ用
import logging
logging.basicConfig(level=logging.DEBUG)


def index(request):
    context = {}
    return render(request, "index.html", context)


def memo(request):
    context = {}
    context["dataset"] = Note.objects.all().order_by('-id')
    return render(request, "memo/index.html", context)


def memo_detail(request, id):
    context = {}
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
    context = {}
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
        # logging.debug(clst)
        # IN句
        qs = Question.objects.filter(cat_id__in=clst)
        # logging.debug(a)
    else:
        qs = Question.objects.all()
        # logging.debug("空です")

    ret = {"qa_json": serializers.serialize('json', qs)}
    # ret = serializers.serialize('json', qs)

    return JsonResponse(ret)


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
    paginator = Paginator(queryset.filter(hoge__icontains=q), 100)

    try:
        dataset = paginator.page(page)
    except PageNotAnInteger:
        dataset = paginator.page(1)
    except EmptyPage:
        dataset = paginator.page(paginator.num_pages)

    context = {}
    context["dataset"] = dataset

    return render(request, "qa/list.html", context)


def qa_detail(request, id):
    context = {}
    context["data"] = Question.objects.get(id=id)
    return render(request, "qa/detail.html", context)
