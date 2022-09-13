from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post


@receiver(post_save, sender=Post)
def on_style_save(sender, instance, created, **kwargs):
    instance.generate_thumbnail(save=True)
