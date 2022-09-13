from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Page


@receiver(post_save, sender=Page)
def on_style_save(sender, instance, created, **kwargs):
    pass
