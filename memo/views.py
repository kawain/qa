from django.shortcuts import render

# from django.http import HttpResponse
# return HttpResponse("")


def index(request):
    context = {}
    return render(request, "index.html", context)


def memo(request):
    context = {}
    return render(request, "memo/index.html", context)


def qa(request):
    context = {}
    return render(request, "qa/index.html", context)
