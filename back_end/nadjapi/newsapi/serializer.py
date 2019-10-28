from rest_framework import serializers
from .models import Articles, ArticlesFromApi

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ('__all__')


class ArticlesFromApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlesFromApi
        fields = ('__all__')