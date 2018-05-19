#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.conf import settings
# Create your views here.


def global_setting(request):
    '''
    博客全局设置
    '''
    return {'SITE_NAME':settings.SITE_NAME,
            'SITE_DESC':settings.SITE_DESC,
            'WEIBO_SINA':settings.WEIBO_SINA,
            'WEIBO_TECENT':settings.WEIBO_TECENT,
            'PRO_RSS':settings.PRO_RSS,
            'PRO_EMAIL':settings.PRO_EMAIL,}

class IndexPageView(View):
    '''
    博客index页面
    '''
    def get(self,request):
        return render(request,"index.html",locals())