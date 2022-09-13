from rest_framework import serializers
from tools.validators import grecaptcha_validator
from .models import Subscriber


class CreateSubscriberSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, write_only=True, min_length=2, max_length=255)
    token = serializers.CharField(write_only=True, required=True, validators=[grecaptcha_validator()])

    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'token']
