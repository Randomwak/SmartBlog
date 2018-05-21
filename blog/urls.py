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
    #文章详情页面
    url(r'^article/$', ArticleView.as_view(), name='article'),
    #评论提交
    url(r'^comment/post/$', CommentPostView.as_view(), name='comment_post'),
    #标签页面
    url(r'^tag/$',TagView.as_view(),name='tag')
]