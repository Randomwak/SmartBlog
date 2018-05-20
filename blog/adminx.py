#-*- coding:utf-8 -*-
import xadmin
from .models import Tag,Ad,Links,Comment,Article,Category

from xadmin import views

class BaseSetting(object):
    '''
    启用主题设置
    '''
    enable_themes=True
    use_bootswatch=True

class GlobalSettings(object):
    '''
    后台全局设置
    '''
    site_title=u"后台管理系统"
    site_footer=u"SmartBlog"
    menu_style="accordion"  #收藏夹式



#注册相应数据模型
xadmin.site.register(Tag)
xadmin.site.register(Ad)
xadmin.site.register(Links)
xadmin.site.register(Category)
xadmin.site.register(Comment)
xadmin.site.register(Article)

#配置后台
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)