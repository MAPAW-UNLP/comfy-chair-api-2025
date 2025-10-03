from rest_framework import serializers
from conference_sessions.models import Session
from users.models import User
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    notification_author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    session = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'main_file_url', 'status', 'article_type',
            'abstract', 'source_file_url', 'authors', 'notification_author', 'session'
        ]
