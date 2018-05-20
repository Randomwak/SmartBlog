#-*- coding:utf-8 -*-
"""SmartBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from blog.views import IndexPageView,ArchiveView

import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #配置博客主页
    url(r'^index/$',IndexPageView.as_view(),name="index"),
    #文章归档页面
    url(r'^archive/$', ArchiveView.as_view(), name="archive"),
    url(r'', include('ckeditor_uploader.urls')),       #富文本编辑器
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #没有这一句无法显示上传的图片


