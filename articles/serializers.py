from rest_framework import serializers
from conference_sessions.models import Session
from conference_sessions.serializers import SessionSerializer
from users.models import User
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    notification_author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    # Para lectura
    session = SessionSerializer(read_only=True)

    # Para escritura
    session_id = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all(), source='session', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'main_file', 'status', 'article_type',
            'abstract', 'source_file', 'authors', 'notification_author',
            'session', 'session_id'
        ]
