from django.db import models
import uuid

# Create your models here.
class Cluster(models.Model):
    cluster_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cluster_headline = models.CharField(max_length=250, blank=True, null=True)
    cluster_summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.cluster_headline

class NewsSummary(models.Model):
    news_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    headline = models.CharField(max_length=250)
    summary = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    pub_date = models.DateTimeField("Date Published", blank=True, null=True)
    sum_date = models.DateTimeField("Date Summarized", auto_now_add=True)
    category = models.CharField(max_length=20)
    cluster_id = models.ForeignKey(Cluster, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.headline

class User(models.Model):
    user_id = models.CharField(max_length=40, primary_key=True)

    def __str__(self):
        return self.user_id

class UserRating(models.Model):
    rating_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    news_summary = models.ForeignKey(NewsSummary, on_delete=models.CASCADE)

    def __str__(self):
        return self.score

class Favorite(models.Model):
    favorite_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    news_summary = models.ForeignKey(NewsSummary, on_delete=models.CASCADE)

    def __str__(self):
        return self.news_summary

class Recommend(models.Model):
    recommend_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cluster_id = models.ForeignKey(Cluster, on_delete=models.CASCADE)

    def __str__(self):
        return self.cluster_id