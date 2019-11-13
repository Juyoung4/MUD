from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, filters
from .models import  NewsSummary, Cluster, User, UserRating, Favorite, Recommend
from .serializer import  NewsSummarySerializer, ClusterSerializer, UserSerializer, UserRatingSerializer, FavoriteSerializer, RecommendSerializer
import requests
import json
import random
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
def index(request):
    return HttpResponse("News Articles App")
    
class Summary(viewsets.ModelViewSet):
    queryset = NewsSummary.objects.all()
    serializer_class = NewsSummarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'news_id', 'cluster_id']
    search_fields = ['headline', 'pub_date']
    ordering = ['pub_date']

class RegisterdUsers(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class NewsCluster(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cluster_id']
    search_fields = ['cluster_headline']

class RatingList(viewsets.ModelViewSet):
    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id', 'news_summary']

class FavoriteList(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id', 'news_summary']

class RecommendList(viewsets.ModelViewSet):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id', 'cluster_id']
