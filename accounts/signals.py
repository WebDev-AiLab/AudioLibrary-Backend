from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from accounts.models import User, UserVerificationData
from tools.location import get_location
from tools.user import send_user_restore_email, send_user_verification_email, create_verification_token, \
    sync_data_with_phpbb, delete_user_phpbb, ban_phpbb_user
from settings.auth import VERIFICATION_TOKEN_RESTORE_KEY, VERIFICATION_TOKEN_REGISTRATION_KEY


@receiver(post_save, sender=User)
def signal_sync_data_with_services(sender, instance, created, **kwargs):
    print('signal_sync_data_with_services')
    # sync_data_with_phpbb(instance, created)
    #
    # ban_phpbb_user(instance)


@receiver(post_delete, sender=User)
def signal_delete_user(sender, instance, **kwargs):
    print('signal_delete_user')
    delete_user_phpbb(instance)


@receiver(post_save, sender=User)
def send_verification_token(sender, instance, created, **kwargs):
    if created:
        create_verification_token(VERIFICATION_TOKEN_REGISTRATION_KEY, instance)


@receiver(post_save, sender=UserVerificationData)
def send_verification_email(sender, instance, created, **kwargs):
    if created:

        user = instance.user

        if instance.target == VERIFICATION_TOKEN_RESTORE_KEY:
            send_user_restore_email(instance.token, user.email)

        elif instance.target == VERIFICATION_TOKEN_REGISTRATION_KEY:
            send_user_verification_email(instance.token, user.email)
