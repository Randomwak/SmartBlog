#-*- coding:utf-8 -*-
from django.conf.urls import url
from blog.views import *

urlpatterns = [
    #配置博客主页
    url(r'^$',IndexPageView.as_view(),name="index"),
    #文章归档页面
    url(r'^archive/$', ArchiveView.as_view(), name="archive"),
    #文章分类页面
    url(r'^category/$', CategoryView.as_view(), name='category'),

]