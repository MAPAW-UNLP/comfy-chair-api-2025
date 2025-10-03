from rest_framework import serializers
from conference_sessions.models import Session
from conferences.models import Conference
from users.models import User
from .models import Article

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ['id', 'name' ]

class SessionSerializer(serializers.ModelSerializer):
    conference = ConferenceSerializer(read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'title', 'deadline', 'conference']

class ArticleSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    notification_author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    session = SessionSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'main_file_url', 'status', 'article_type',
            'abstract', 'source_file_url', 'authors', 'notification_author', 'session'
        ]
