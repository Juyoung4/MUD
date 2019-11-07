from rest_framework import serializers
from .models import ArticlesFromApi, NewsSummary, Cluster, User, UserRating, Favorite, Recommend


class ArticlesFromApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlesFromApi
        fields = ('__all__')

class NewsSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSummary
        fields = ('id', 'headline', 'summary', 'url', 'pub_date', 'sum_date', 'category')

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ('__all__')

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('__all__')

class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = ('__all__')