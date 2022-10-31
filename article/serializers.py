from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Feed, Article


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

    follows = IntegerField(source='follows.count', read_only=True)


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article

    likes = IntegerField(source='likes.count', read_only=True)

    exclude = ('reads', )
