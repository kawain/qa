"""qa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from memo import views

urlpatterns = [
    path('', views.index, name='index'),
    path('memo/', views.memo, name='memo'),
    path('memo/detail/<int:id>/', views.memo_detail, name='memo_detail'),
    path('memo/create/', views.memo_create, name='memo_create'),
    path('qa/', views.qa, name='qa'),
    path('qa/start/', views.qa_start, name='qa_start'),
    path('qa/search/', views.qa_search, name='qa_search'),
    path('qa/detail/<int:id>/', views.qa_detail, name='qa_detail'),
    path('admin/', admin.site.urls),
]
