from .models import Article
from user.models import User
from rest_framework import serializers
from user.serializers import UserSerializer
from conference_session.models import Session
from conference_session.serializers import SessionSerializer
from user.models import User
from user.serializers import UserSerializer
from .models import Article, ArticleDeletionRequest

class ArticleSerializer(serializers.ModelSerializer):

    # Lectura
    session = SessionSerializer(read_only=True)
    authors = UserSerializer(many=True, read_only=True)
    corresponding_author = UserSerializer(read_only=True)

    # Escritura
    session_id = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all(), source='session', write_only=True, required=False, allow_null=True
    )
    authors_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, source='authors', write_only=True
    )
    corresponding_author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='corresponding_author', write_only=True
    )

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'main_file', 'status', 'type',
            'abstract', 'source_file',
            'authors', 'corresponding_author',
            'authors_ids', 'corresponding_author_id',
            'session', 'session_id'
        ]

class ArticleDeletionRequestSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True)
    article_id = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(), source='article', write_only=True
    )

    class Meta:
        model = ArticleDeletionRequest
        fields = [
            'id', 'article', 'article_id', 'description', 
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

