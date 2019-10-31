from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Articles, ArticlesFromApi
from .serializer import ArticlesSerializer, ArticlesFromApiSerializer
import requests
import json
import random
# Create your views here.

def index(request):
    return HttpResponse("Success")

class ArticlesAPI(viewsets.ModelViewSet):
    queryset = ArticlesFromApi.objects.all()
    serializer_class = ArticlesFromApiSerializer

def latest(request):
    try:
        # To Do 
        # Crawling and Summarization
        URL = 'https://newsapi.org/v2/top-headlines?country=kr&apiKey=e12b2ee6e72c4abbb34d3462f8f00120'
        content = requests.get(URL).content
        dataset = json.loads(content)

        articles = dataset['articles']
        counter = 0
        for article in articles:
            counter += 1
            articles = ArticlesFromApi()
            articles.id = (random.randint(100,999) * 100000) + counter
            articles.articles_author = article['author']
            articles.articles_title = article['title']
            articles.articles_description = article['description']
            articles.articles_url = article['url']
            articles.save()
            
        
        return HttpResponse(f"Data Fetched Successfully. {counter} Articles")
    except Exception as e:
        return HttpResponse(f"Data Not Fetched {e}")