from rest_framework import serializers
from .models import Guest, User, UserVerificationData, UserContactForm
from interactions.serializers import VoteSerializer
from tools.visitor import get_visitor_ip_address
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ObjectDoesNotExist
from tools.user import create_verification_token
from settings.auth import VERIFICATION_TOKEN_RESTORE_KEY
from django.utils.translation import gettext as _
from django.utils import timezone

from tools.validators import email_exists_validator, grecaptcha_validator, validate_username_reserved


class UserPublicLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_guest', 'date_joined']


class UserPrivateSerializer(serializers.ModelSerializer):
    likes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'is_guest', 'is_staff', 'likes']


class CreateGuestSerializer(serializers.ModelSerializer):
    operating_system = serializers.CharField(max_length=1024, required=True)
    browser = serializers.CharField(max_length=1024, required=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Guest
        fields = ['id', 'operating_system', 'browser']

    def create(self, validated_data):
        validated_data['ip'] = get_visitor_ip_address(self.context['request'])
        return super(CreateGuestSerializer, self).create(validated_data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message=_('Email is already taken'))]
    )
    # do not validate password - let user decide what is good
    # i think it is a good practice, but we'll see
    password = serializers.CharField(write_only=True, required=True, min_length=6, max_length=255)
    username = serializers.CharField(write_only=True, required=True, min_length=4, validators=[
        UniqueValidator(queryset=User.objects.all(), message=_('Username is already taken')), validate_username_reserved])
    captcha = serializers.CharField(write_only=True, required=True, validators=[grecaptcha_validator()])

    # this url will be sent to user to verify registration, should be included into POST
    # callback = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'captcha']

    def create(self, validated_data):
        user = User.objects.create(
            is_active=False,  # active by default
            is_guest=False,
            username=validated_data['username'],
            last_login=timezone.now(),
            email=validated_data['email']
        )

        # hash and save password
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserVerificationSerializer(serializers.ModelSerializer):
    secret = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = UserVerificationData
        fields = ['secret']

    def verify(self, validated_data):
        try:
            # todo use verification data object
            user = User.objects.get(verification__token=validated_data['secret'], is_verified=False)
            user.is_verified = True
            user.is_active = True
            user.save()
            return True
        except ObjectDoesNotExist:
            return False


class UserRestorePasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[email_exists_validator(User)])
    token = serializers.CharField(write_only=True, required=True, validators=[grecaptcha_validator()])

    class Meta:
        model = User
        fields = ['email', 'token']

    def restore(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
            token = create_verification_token(VERIFICATION_TOKEN_RESTORE_KEY, user)
            # notify_user(token.token, validated_data['email'])
            return True
        except ObjectDoesNotExist:
            return False


class UserDeactivateSerializer(serializers.ModelSerializer):
    secret = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['secret']

    def deactivate(self, validated_data):
        try:
            verification_data = UserVerificationData.objects.get(token=validated_data['secret'],
                                                                 target=VERIFICATION_TOKEN_RESTORE_KEY)
            user = verification_data.user
            user.is_active = False
            user.save()
            return True
        except ObjectDoesNotExist:
            return False


# todo move it to user, probably
class UserChangePasswordSerializer(serializers.ModelSerializer):
    secret = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=6, max_length=255)
    captcha = serializers.CharField(write_only=True, required=True, validators=[grecaptcha_validator()])

    class Meta:
        model = User
        fields = ['secret', 'captcha', 'password']

    def change_password(self, validated_data):
        try:
            verification_data = UserVerificationData.objects.get(token=validated_data['secret'],
                                                                 target=VERIFICATION_TOKEN_RESTORE_KEY,
                                                                 user__is_active=False)
            user = verification_data.user
            user.set_password(validated_data['password'])
            user.is_active = True  # activate again
            user.save()

            # delete verification data
            verification_data.delete()
            return True
        except ObjectDoesNotExist:
            return False


class CreateApplicationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, write_only=True, min_length=2, max_length=255)
    text = serializers.CharField(required=True, write_only=True)
    name = serializers.CharField(required=True, write_only=True, max_length=255)
    subject = serializers.CharField(required=True, write_only=True, max_length=255)

    token = serializers.CharField(write_only=True, required=True, validators=[grecaptcha_validator()])

    class Meta:
        model = UserContactForm
        fields = ['email', 'text', 'name', 'subject', 'token']

    def create(self, validated_data):
        return UserContactForm.objects.create(
            user=self.context['request'].user,
            email=validated_data['email'],
            name=validated_data['name'],
            subject=validated_data['subject'],
            text=validated_data['text'],
            ip=get_visitor_ip_address(self.context['request'])
        )
