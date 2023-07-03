from django.contrib import admin
# from DjangoUeditor import urls
from django.views.generic import RedirectView
from django.views.static import serve
from .settings import MEDIA_ROOT  # import MEDIA_ROOT from settings
from article import urls
from django.contrib import admin
from django.urls import path, include
from article import views
from webapp1 import views as mainView
from django.urls import re_path as url
from django.conf import settings
from django.views.static import serve
from .settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', mainView.index),
    path('',mainView.index),
    path('login/',mainView.login),
    path('signup/',mainView.signUp),
    path('logout/',mainView.signout),
    path('article/', include('article.urls', namespace='article')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('ueditor/', include('DjangoUeditor.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
