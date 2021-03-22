from django.shortcuts import render

# from django.http import HttpResponse
# return HttpResponse("")

from .models import Category, Tag, Question, Note
from .forms import NoteForm


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
    return render(request, "qa/index.html", context)
