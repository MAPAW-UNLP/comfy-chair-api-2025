from rest_framework import serializers
from .models import ReviewScore
from article.models import Article
from user.models import User

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'affiliation', 'role']

class ArticleNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'type', 'status', 'abstract']

class ReviewScoreSerializer(serializers.ModelSerializer):
    user = UserNestedSerializer(read_only=True)
    article = ArticleNestedSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    article_id = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), source='article', write_only=True)

    class Meta:
        model = ReviewScore
        fields = [
            'id', 'user', 'article', 'score',
            'user_id', 'article_id'
        ]
        read_only_fields = ['id']
