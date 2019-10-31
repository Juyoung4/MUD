from django.db import models

# Create your models here.
class ArticlesFromApi(models.Model):
    id = models.IntegerField(primary_key=True)
    articles_author = models.CharField(max_length=40, null=True, blank=True)
    articles_title = models.CharField(max_length=200, null=True, blank=True)
    articles_description = models.CharField(max_length=1000, null=True, blank=True)
    articles_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.articles_title
