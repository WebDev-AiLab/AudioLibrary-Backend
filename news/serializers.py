from rest_framework import serializers

from accounts.serializers import UserPublicLightSerializer
from news.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserPublicLightSerializer()

    class Meta:
        model = Post
        exclude = ['updated']


class PostListingSerializer(serializers.ModelSerializer):
    author = UserPublicLightSerializer()

    class Meta:
        model = Post
        fields = ['id', 'slug', 'title', 'created', 'author', 'excerpt', 'picture', 'picture_thumbnail']