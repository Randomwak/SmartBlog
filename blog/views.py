#-*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.conf import settings
from django.db.models import Count
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, login, authenticate
from models import Category,Ad,Article,Links,Comment,Tag,UserProfile
from django.contrib.auth.hashers import make_password
from forms import *
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
    try:
        comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
        #把comment对象取出来到article对象中进行查找，可使用pirnt comment_count_list来查看
        article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list][:6]
    except:
        article_comment_list=[]

    #站长推荐
    recommend_articles=Article.objects.filter(is_recommend=True)[:6]

    #浏览排行
    click_articles_list=Article.objects.all().order_by('-click_count')[:6]

    #文章归档数据
    archive_list = Article.objects.distinct_date()

    #文章标签数据
    tag_list=Tag.objects.all()

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
            'tag_list':tag_list,
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


class ArticleView(View):
    '''
    文章详情页面
    '''
    def get(self,request):
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(pk=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})


        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})

        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)

        comment_num=article.comment_set.all().count()
        return render(request, 'article.html', {
            'article':article,
            'comment_list':comment_list,
            'comment_num':comment_num,
            'comment_form':comment_form,
        })


class CommentPostView(View):
    '''
    提交评论
    '''
    def post(self,request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
        return redirect(request.META['HTTP_REFERER'])

class TagView(View):
    '''
    获取标签页面
    '''
    def get(self,request):
        # 获取标签id
        name = request.GET.get('tname', None)
        article_list=Article.objects.filter(tag__name=name)
        article_list=getPage(request,article_list)

        return render(request,"tag.html",{
            'article_list':article_list,
        })




class RegisterView(View):
    '''
    注册
    '''
    def post(self,request):
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            # 注册
            user = UserProfile.objects.create(username=reg_form.cleaned_data["username"],
                                       email=reg_form.cleaned_data["email"],
                                       url=reg_form.cleaned_data["url"],
                                       password=make_password(reg_form.cleaned_data["password"]), )
            user.save()

            # 登录
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
            login(request, user)
            return redirect(request.POST.get('source_url'))
        else:
            return render(request, 'failure.html', {'reason': reg_form.errors})

        return render(request, 'reg.html', locals())

    def get(self,request):
        reg_form = RegForm()
        return render(request, 'reg.html', locals())


class LoginView(View):
    '''
    登录
    '''
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 登录
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
            else:
                return render(request, 'failure.html', {'reason': '登录验证失败'})
            return redirect(request.POST.get('source_url'))
        else:
            return render(request, 'failure.html', {'reason': login_form.errors})
        render(request, 'login.html', locals())

    def get(self,request):
        login_form = LoginForm()
        return render(request, 'login.html', locals())


class LogoutView(View):
    '''
    登出
    '''
    def get(self,request):
        logout(request)
        return redirect(request.META['HTTP_REFERER'])
