from rest_framework import serializers
from .models import Vote, Comment


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['track']
