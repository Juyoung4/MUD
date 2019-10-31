from rest_framework import serializers
from .models import ArticlesFromApi


class ArticlesFromApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlesFromApi
        fields = ('__all__')

