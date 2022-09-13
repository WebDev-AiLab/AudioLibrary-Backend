from requests import JSONDecodeError

from settings import SITE_URL_FRONTEND, SITE_NAME, VERIFICATION_TOKEN_REGISTRATION_KEY, FRONTEND, MISAGO_URL, FORUM_URL, \
    FORUM_CANARY
from accounts.models import UserVerificationData
from django.template.loader import render_to_string
from tools.mail import send_html_email
from django.utils.translation import gettext as _
import requests

from tools.string import generate_random_string


def create_verification_token(target, user):
    return UserVerificationData.objects.create(
        target=target,
        user=user
    )


# todo replace with signals
def send_user_verification_email(token, email):
    verification_url = f"{FRONTEND['verification_url']}secret={token}"
    subject = f"Welcome to {SITE_NAME}!"
    html = render_to_string('email_verification_registration.html', {
        'header': subject,
        'text_1': _('Someone has created account using your email.'),
        'text_2': _('If it wasn\'t you, simply ignore this email.'),
        'action': _('If you did make this request just click the button below:'),
        'button': _('ACTIVATE MY ACCOUNT'),
        'button_link': verification_url,
        'text_small': _(
            'If you didn\'t request any changes, you don\'t have to do anything. So that\'s easy.'),
    })
    send_html_email(email, subject=subject, html=html)


def send_user_restore_email(token, email):
    subject = "Forgot your password?"
    verification_url = FRONTEND['password_restore_url'] + 'secret=' + token
    html = render_to_string('email_verification_registration.html', {
        'header': _('Forgot your password?'),
        'text_1': _('We received a request to reset your password.'),
        'text_2': _('If you didn\'t make this request, simply ignore this email.'),
        'action': _('If you did make this request just click the button below:'),
        'button': _('RESET MY PASSWORD'),
        'button_link': verification_url,
        'text_small': _(
            'If you didn\'t request to change your brand password, you don\'t have to do anything. So that\'s easy.'),
    })
    send_html_email(email, subject=subject, html=html)


def sync_data_with_phpbb(user, created=False):
    params = {
        'id': user.phpbb_id,
        'username': user.username,
        'email': user.email,
        'password': user._raw_password,
        '_canary': FORUM_CANARY
        # todo other fields
    }

    action = 'create' if user.phpbb_id is None else 'update'
    response = requests.post(f"{FORUM_URL}/app.php/restApiV1/users/{action}", data=params)
    print(response.content)

    try:
        response = response.json()
    except JSONDecodeError:
        # print('something went wrong with phpbb')
        # print(response.content)
        return None

    phpbb_id = response.get('id', None)
    if phpbb_id:
        user.phpbb_id = phpbb_id
        user.save()


def generate_xs_signin_token(user):
    token = generate_random_string(64)
    pass  # todo


def delete_user_phpbb(user):
    if not user.phpbb_id:
        return None

    params = {
        'id': user.phpbb_id,
        '_canary': FORUM_CANARY
    }

    response = requests.post(f"{FORUM_URL}/app.php/restApiV1/users/delete", data=params)
    try:
        response = response.json()
        # todo
    except JSONDecodeError:
        return None


def ban_phpbb_user(user):
    if not user.banned_by_ip:
        return None

    print(user.ip)

    params = {
        'id': user.phpbb_id,
        'u': user.banned_by_ip,
        'ip_address': user.ip,
        '_canary': FORUM_CANARY
    }

    response = requests.post(f"{FORUM_URL}/app.php/restApiV1/users/ban", data=params)
    print(response.content)
    try:
        response = response.json()
        # todo
    except JSONDecodeError:
        return None
