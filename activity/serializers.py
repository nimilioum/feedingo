from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message', 'user']

    user = SlugRelatedField(many=False, slug_field='username', read_only=True)
