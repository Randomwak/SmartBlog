#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.conf import settings

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from models import Category,Ad,Article
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
        #分类数据
        category_list=Category.objects.all()
        #广告数据
        ad_list=Ad.objects.all()


        #最新文章数据
        artical_list=Article.objects.all()

        #获取页面
        try:
            page = request.GET.get('page', 1)
        except (PageNotAnInteger,EmptyPage):
            page = 1

        #分页
        p = Paginator(artical_list,3, request=request)

        artical_list=p.page(page)

        return render(request,"index.html",{
            'category_list':category_list,
            'ad_list':ad_list,
            'artical_list':artical_list,
        })

