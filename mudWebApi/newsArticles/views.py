from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import ArticlesFromApi
from .serializer import ArticlesFromApiSerializer
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