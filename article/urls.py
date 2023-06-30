from django.urls import re_path as url
from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    url(r'^$', views.article_list),
    # path used to import url to the view
    path('article-list/', views.article_list, name='article_list'),
    # article detail
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    # delete article
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    # create article
    path('create/', views.create, name='reate'),
    # update article
    path('article-update/<int:id>/', views.article_update, name='article_update'),
]