

import xadmin
from .models import Tag,Ad,Links,Comment,Article,Category

xadmin.site.register(Tag)
xadmin.site.register(Ad)
xadmin.site.register(Links)
xadmin.site.register(Category)
xadmin.site.register(Comment)
xadmin.site.register(Article)
