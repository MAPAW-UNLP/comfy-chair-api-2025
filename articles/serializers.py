from rest_framework import serializers
from users.models import User
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )
    notification_author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "session_name",
            "main_file_url",
            "status",
            "abstract",
            "source_file_url",
            "authors",
            "notification_author",
        ]
