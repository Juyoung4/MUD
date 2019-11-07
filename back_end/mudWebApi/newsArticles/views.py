from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .models import ArticlesFromApi, NewsSummary, Cluster, User, UserRating, Favorite, Recommend
from .serializer import ArticlesFromApiSerializer, NewsSummarySerializer, ClusterSerializer, UserSerializer, UserRatingSerializer, FavoriteSerializer, RecommendSerializer
import requests
import json
import random

# Create your views here.

counter = 0

def index(request):
    return HttpResponse("News Articles App")

class ArticlesAPI(viewsets.ModelViewSet):
    queryset = ArticlesFromApi.objects.all()
    serializer_class = ArticlesFromApiSerializer

class Summary(viewsets.ModelViewSet):
    queryset = NewsSummary.objects.all()
    serializer_class = NewsSummarySerializer

class RegisterdUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class NewsCluster(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

class RatingList(viewsets.ModelViewSet):
    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer

class FavoriteList(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class RecommendList(viewsets.ModelViewSet):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer

def latest(request):
    global counter
    try:
        # To Do 
        # Crawling and Summarization
        URL = 'https://newsapi.org/v2/top-headlines?country=kr&apiKey=e12b2ee6e72c4abbb34d3462f8f00120'
        content = requests.get(URL).content
        dataset = json.loads(content)

        articles = dataset['articles']
        for article in articles:
            counter += 1
            articles = ArticlesFromApi()
            articles.id = (random.randint(100,999) * 10000) + counter
            articles.articles_author = article['author']
            articles.articles_title = article['title']
            articles.articles_description = article['description']
            articles.articles_url = article['url']
            print(f'Save Aeticle Number : {counter} Title : {article["title"]} Url : {article["url"]} ')
            articles.save()
            
        
        return HttpResponse(f"Data Fetched Successfully. {counter} Articles")
    except Exception as e:
        return HttpResponse(f"Data Not Fetched {e}")