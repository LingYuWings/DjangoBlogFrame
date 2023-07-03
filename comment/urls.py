from django.urls import path
from . import views

# the app name that is deploying
app_name = 'comment'

urlpatterns = [
    # leave comment that links to the article
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
]