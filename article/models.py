from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# timezone used to deal with the work related with time
from django.utils import timezone
from django.urls import reverse

# blog article data model
class ArticlePost(models.Model):
    # article author, on_delete use to define the way to delete the data
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # article title
    title = models.CharField(max_length=100)

    # article body, textfield used to storage large amount of text data
    body = models.TextField()

    # article created time
    created = models.DateTimeField(default=timezone.now)

    # article last updated time
    updated = models.DateTimeField(auto_now=True)

    # article total views, default is 0
    total_views = models.PositiveIntegerField(default=0)

    # class Meta used to define metadata of the model
    class Meta:
        # ordering define the way sorting the data which the model return
        # '-created' define the most recent created article will be display on the top
        ordering = ('-created',)

    # __str__ define the retuen value when using str() function
    def __str__(self):
        # return self.title return the article title
        return self.title

        # get the article url
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])