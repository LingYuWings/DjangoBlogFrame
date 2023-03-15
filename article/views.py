from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# 导入数据模型ArticlePost
from comment.models import Comment
from . import models
from .models import ArticlePost
# 引入User模型
from django.contrib.auth.models import User
# 引入分页模块
from django.core.paginator import Paginator
from article.form import ContentForm
from django.contrib import messages

def article_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'total_views':
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'

    paginator = Paginator(article_list, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 修改此行
    context = { 'articles': articles, 'order': order }

    return render(request, 'list.html', context)


    
def create(request):
    context = {
        'content_form': ContentForm()
    }

    if request.method == 'GET': # 获取空界面用于创建该文章的内容
        return render(request, 'create.html', context=context)
    if request.method == 'POST':    # 新建文章
        new_article_title = request.POST.get('title')
        new_article_body = request.POST.get('body')
        new_article_author = User.objects.get(id=request.user.id)
        if new_article_title != None and new_article_body!= None:
            models.ArticlePost.objects.create(title=new_article_title, body=new_article_body,author=new_article_author)
        else:
            error_msg='标题及内容不能为空'
            return redirect("/article/create/",{'error_msg':error_msg})

        return redirect("article:article_list")


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 取出文章评论
    comments = Comment.objects.filter(article=id)

    # 需要传递给模板的对象
    # context = { 'article': article }
    context = { 'article': article, 'comments': comments }
    # 载入模板，并返回context对象
    return render(request, 'detail.html', context)

# 删文章
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return redirect("article:article_list")
    else:
        # 调用.delete()方法删除文章
        article.delete()
        # 完成删除后返回文章列表
        return redirect("article:article_list")
# 更新文章
# 提醒用户登录
@login_required(login_url='webapp1/login/')

def article_update(request, id):
    # # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponseRedirect("article:article_list")
    
    context = {
        'article': ArticlePost.objects.get(id=id),
        'content_form': ContentForm()
    }


    # 判断用户是否为 POST 提交表单数据
    if request.method == 'GET': # 获取空界面用于创建该文章的内容
        return render(request, 'update.html', context=context)
    elif request.method == 'POST':
        new_article_title = request.POST.get('title')
        new_article_body = request.POST.get('body')
        if new_article_title != None and new_article_body!= None:
            ArticlePost.objects.filter(id=id).update(title=new_article_title, body=new_article_body)
        else:
            error_msg='标题及内容不能为空'
            return redirect("/article/article-update/"+str(id),{'error_msg':error_msg})
    return redirect("/article/article-detail/"+str(id))
