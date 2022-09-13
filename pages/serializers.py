from rest_framework import serializers
from .models import Page
from accounts.serializers import UserPublicLightSerializer


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = ['is_deletable', 'updated']


class PageLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'slug', 'url_mask', 'page', 'type', 'title', 'created', 'section']

