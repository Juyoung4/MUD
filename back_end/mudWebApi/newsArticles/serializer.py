from rest_framework import serializers
from .models import NewsSummary, Cluster, User, UserRating, Favorite, Recommend


class NewsSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSummary
        fields = ('__all__')
        #fields = ('id', 'headline', 'summary', 'url', 'pub_date', 'sum_date', 'category')

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