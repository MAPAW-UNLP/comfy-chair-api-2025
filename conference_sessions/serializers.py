from rest_framework import serializers
from .models import ConferenceSession
from articles.serializers import ArticleSerializer

class ConferenceSessionSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = ConferenceSession
        fields = ['id', 'title', 'deadline', 'conference_title', 'articles']

class ConferenceSessionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceSession
        fields = ['title', 'deadline', 'conference_title', 'articles']
