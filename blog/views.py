#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.


class IndexPageView(View):
    '''
    博客index页面
    '''
    def get(self,request):
        return render(request,"index.html",locals())