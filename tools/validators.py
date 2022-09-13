from accounts.models import RESERVED_NAMES
from settings.captcha import GRECAPTCHA_SECRET, GRECAPTCHA_URL
from .visitor import get_visitor_ip_address
from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _

import requests


def grecaptcha_validator(request=None):
    def validator(value):
        params = {
            'response': value,
            'secret': GRECAPTCHA_SECRET,
            'remoteip': get_visitor_ip_address(request) if request is not None else None
        }

        try:
            response = requests.post(GRECAPTCHA_URL, data=params)
            response = response.json()

            if not response.get('success', False):
                raise ValidationError('CAPTCHA is invalid')

        except requests.exceptions.RequestException as e:
            raise ValidationError('Unable to validate CAPTCHA')

    return validator


def email_exists_validator(user):
    def validator(value):
        try:
            user.objects.get(email=value)
        except ObjectDoesNotExist:
            raise ValidationError(_('User with provided Email does not exist'))

    return validator


def validate_username_reserved(username):
    if username.lower() in RESERVED_NAMES:
        raise ValidationError(f"\"{username}\" is a reserved name and cannot be used")
