from django.contrib import admin
# from DjangoUeditor import urls
from django.views.generic import RedirectView
from django.views.static import serve  # 上传文件处理函数
from .settings import MEDIA_ROOT  # 从配置中导入MEDIA_ROOT
from article import urls
from django.contrib import admin
# 记得引入include
from django.urls import path, include
# 存放映射关系的列表
from article import views
from webapp1 import views as mainView
from django.urls import re_path as url
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', mainView.index),
    # 新增代码，配置app的url
    path('',mainView.index),
    path('login/',mainView.login),
    path('signup/',mainView.signUp),
    path('logout/',mainView.signout),
    path('article/', include('article.urls', namespace='article')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('ueditor/', include('DjangoUeditor.urls')),
]
