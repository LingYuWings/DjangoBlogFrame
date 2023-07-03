from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# import ArticlePost data structure
from comment.models import Comment
from . import models
from .models import ArticlePost
# import user model
from django.contrib.auth.models import User
# import paginator model
from django.core.paginator import Paginator
from article.form import ContentForm
from django.contrib import messages

def article_list(request):
    # return defferent sorted result accroding to the get request
    if request.GET.get('order') == 'total_views':
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'

    paginator = Paginator(article_list, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = { 'articles': articles, 'order': order }

    return render(request, 'list.html', context)


    
def create(request):
    context = {
        'content_form': ContentForm()
    }

    if request.method == 'GET': # get an empty page to create blog content
        return render(request, 'create.html', context=context)
    if request.method == 'POST':    # create new article
        new_article_title = request.POST.get('title')
        new_article_body = request.POST.get('body')
        new_article_author = User.objects.get(id=request.user.id)
        if new_article_title != None and new_article_body!= None:
            models.ArticlePost.objects.create(title=new_article_title, body=new_article_body,author=new_article_author)
        else:
            error_msg='标题及内容不能为空'
            return redirect("/article/create/",{'error_msg':error_msg})

        return redirect("article:article_list")


# article detail
def article_detail(request, id):
    # read the article by id from the database
    article = ArticlePost.objects.get(id=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # search the comment related to the article and write it to the article page
    comments = Comment.objects.filter(article=id)

    # context = { 'article': article }
    context = { 'article': article, 'comments': comments }
    # load template and retuen context
    return render(request, 'detail.html', context)

# delete article
def article_delete(request, id):
    # get the article id the user wanna delete
    article = ArticlePost.objects.get(id=id)
    # if the user is not the article's creator, forbidden the user from delete the article
    if request.user != article.author:
        return redirect("article:article_list")
    else:
        article.delete()
        # finish delete, return to the article list
        return redirect("article:article_list")
    
# article update
# this function require the user logged in
@login_required(login_url='webapp1/login/')

def article_update(request, id):
    # get the article that needed to be update
    article = ArticlePost.objects.get(id=id)
    # only the creator of the article can update it
    if request.user != article.author:
        return HttpResponseRedirect("article:article_list")
    
    context = {
        'article': ArticlePost.objects.get(id=id),
        'content_form': ContentForm()
    }


    # user need to use POST way to submit the updated article
    if request.method == 'GET': 
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
