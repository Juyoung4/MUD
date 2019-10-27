from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Articles
from .serializer import ArticlesSerializer
# Create your views here.

def index(request):
    return HttpResponse("Success")

class ArticlesAPI(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer

def latest(request):
    try:
        articles = Articles()
        articles.author = "Test Data"
        articles.title = "Test Data"
        articles.description = "Test Data"
        articles.url = "Test Data"
        articles.urlToImage = "Test Data"
        articles.publishedAt = "Test Data"
        articles.content = "Test Data"

        articles.save()
        return HttpResponse("Data Fetched")
    except:
        return HttpResponse("Data Not Fetched")