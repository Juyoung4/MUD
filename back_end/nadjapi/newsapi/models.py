from django.db import models

# Create your models here.
class Articles(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    urlToImage = models.CharField(max_length=300)
    publishedAt = models.CharField(max_length=300)
    content = models.CharField(max_length=600)

    def __str__(self):
        return self.title

class ArticlesFromApi(models.Model):
    id = models.IntegerField
    articles_author = models.CharField(max_length=40, null=True, blank=True)
    articles_title = models.CharField(max_length=200, null=True, blank=True)
    articles_description = models.CharField(max_length=1000, null=True, blank=True)
    articles_url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.articles_title