#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.conf import settings
from django.db.models import Count
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from models import Category,Ad,Article,Links,Comment
# Create your views here.


def global_setting(request):
    '''
    博客全局设置
    '''

    # 分类数据
    category_list = Category.objects.all()
    # 广告数据
    ad_list = Ad.objects.all()
    # 友情链接
    link_list = Links.objects.all()

    #先取出comment中的article，然后使用聚合函数对article进行统计，取生成变量名为comment_count，最后对comment_count进行排序
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    #把comment对象取出来到article对象中进行查找，可使用pirnt comment_count_list来查看
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list][:6]

    #站长推荐
    recommend_articles=Article.objects.filter(is_recommend=True)[:6]

    #浏览排行
    click_articles_list=Article.objects.all().order_by('-click_count')[:6]

    #文章归档数据
    archive_list = Article.objects.distinct_date()

    return {'SITE_NAME':settings.SITE_NAME,
            'SITE_DESC':settings.SITE_DESC,
            'WEIBO_SINA':settings.WEIBO_SINA,
            'WEIBO_TECENT':settings.WEIBO_TECENT,
            'PRO_RSS':settings.PRO_RSS,
            'PRO_EMAIL':settings.PRO_EMAIL,
            'category_list':category_list,
            'ad_list':ad_list,
            'link_list':link_list,
            'article_comment_list':article_comment_list,
            'recommend_articles':recommend_articles,
            'click_articles_list':click_articles_list,
            'archive_list':archive_list,
            }

class IndexPageView(View):
    '''
    博客index页面
    '''
    def get(self,request):
        #最新文章数据
        article_list=Article.objects.all()
        article_list = getPage(request, article_list)

        return render(request,"index.html",{
            'article_list':article_list,
        })

class ArchiveView(View):
    '''
    文章归档
    '''
    def get(self,request):
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list=Article.objects.filter(date_publish__icontains=year+'-'+month)
        article_list=getPage(request,article_list)

        return render(request,"archive.html",{
            'article_list':article_list,
        })


# 分页代码
def getPage(request, article_list):
    # 获取页面
    try:
        page = request.GET.get('page', 1)
    except (PageNotAnInteger, EmptyPage):
        page = 1
    # 分页
    p = Paginator(article_list, 3, request=request)
    article_list = p.page(page)
    return article_list


class CategoryView(View):
    '''
    分类页面
    '''
    def get(self,request):
        # 先获取客户端提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request, article_list)

        return render(request,"category.html",{
            'article_list':article_list,
            'cid':int(cid)-1,
        })