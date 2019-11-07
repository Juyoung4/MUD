from django.urls import path, include
from .views import index, ArticlesAPI, latest, Summary, RegisterdUsers, NewsCluster, FavoriteList, RatingList, RecommendList
from rest_framework import routers

router = routers.DefaultRouter()
router.register("articles", ArticlesAPI)
router.register("summary", Summary)
router.register("users", RegisterdUsers)
router.register("newscluster", NewsCluster)
router.register("favorite", FavoriteList)
router.register("rating", RatingList)
router.register("recommend", RecommendList)

urlpatterns = [
    path('', index, name="index"),
    path('', include(router.urls)),
    path('latest', latest, name="latest"),
]