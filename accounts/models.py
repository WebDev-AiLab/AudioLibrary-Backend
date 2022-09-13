from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from tools.basemodels import GenericUUIDModel, GenericIPCatcher
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext as _
from tools.basemodels import GenericUUIDModel, GenericIDModel
from tools.string import generate_random_string
from settings import VERIFICATION_TOKEN_EXPIRATION_TIME
from django.utils import timezone
from django.contrib.auth.hashers import make_password

username_validator = UnicodeUsernameValidator()

RESERVED_NAMES = [
    'admin', 'administrator', 'user', 'guest', 'audiolibrary', 'bitch',
]


# class Guest(GenericUUIDModel, GenericIPCatcher):
#     browser = models.CharField(max_length=255, null=True, blank=True)
#     operating_system = models.CharField(max_length=255, null=True, blank=True)


class User(AbstractUser, GenericUUIDModel, GenericIPCatcher):
    # forum id, since forum is another service
    phpbb_id = models.IntegerField('PHPBB ID', blank=True, null=True, unique=True)
    # other data
    is_guest = models.BooleanField(_('Guest'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)  # notice that true by default
    is_verified = models.BooleanField(_('Verified by Email'), default=False)

    # copied from user itself
    date_joined = models.DateTimeField(_("Registration Date"), default=timezone.now)
    username = models.CharField(
        _("login"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    # get rid of username, i think we don't need it (at least for now)
    # username = None
    # USERNAME_FIELD = 'email'

    # from guest
    browser = models.CharField(max_length=255, null=True, blank=True)
    operating_system = models.CharField(max_length=255, null=True, blank=True)
    last_seen = models.DateTimeField('Last seen', auto_now=True, db_index=True)

    # also some data
    country = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255, null=True, blank=True)
    utc_offset = models.CharField('UTC offset', max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    banned_by_ip = models.BooleanField(default=False)

    # !!! NOTE !!!
    # the client is willing to save raw password
    # i know it is not secure, but it is not my fault
    _raw_password = models.CharField('Raw Password', max_length=512, null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password  # this will be deleted by parent class
        self._raw_password = raw_password

    def save(self, *args, **kwargs):
        super(User, self).save()

        if self.is_superuser:
            # this is mostly for createsuperuser function
            # there's no need to override it entirely, but just check 'is_superuser' field
            # but if someone will decide to set is_guest manually to a superuser it fill reset the flag as well
            # i think it is ok for me
            self.is_guest = False

        # this is the weird one, but it it temporary
        # todo probably change uuid to id or calculate numeric id somehow
        # if self.is_guest and not self.username:
        #     self.username = f"Guest {self.id}"

        if not self.is_superuser and self.username.lower() in RESERVED_NAMES:
            raise Exception(f"Username \"{self.username}\" is reserved")

        super(User, self).save()


class UserGroup(Group):
    class Meta:
        proxy = True


class Guest(User):
    class Meta:
        proxy = True


class UserOnline(User):
    class Meta:
        proxy = True
        verbose_name = 'User Online'
        verbose_name_plural = 'Users Online'


class UserVerificationData(GenericIDModel):
    user = models.ForeignKey(User, related_name='verification', on_delete=models.CASCADE)
    token = models.CharField(max_length=255, editable=False, unique=True)
    target = models.CharField(max_length=50, db_index=True)

    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'pending'),
        ('sent', 'sent'),
        ('completed', 'completed')
    )
    status = models.CharField(choices=VERIFICATION_STATUS_CHOICES, max_length=10,
                              default=VERIFICATION_STATUS_CHOICES[0][0], db_index=True)

    def save(self, *args, **kwargs):
        self.token = generate_random_string()
        super(UserVerificationData, self).save()

    @property
    def is_expired(self):
        dif = (timezone.now() - self.created).total_seconds()
        return dif > VERIFICATION_TOKEN_EXPIRATION_TIME


class UserContactForm(GenericUUIDModel, GenericIPCatcher):
    user = models.ForeignKey(User, related_name='contact', on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    text = models.TextField()
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Appeal'
