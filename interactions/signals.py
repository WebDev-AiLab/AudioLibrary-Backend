from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Play, Vote, Stat


@receiver(post_save, sender=Play)
def on_play_created(sender, instance, created, **kwargs):
    if created:
        Stat.objects.create(
            type='play', play=instance, track=instance.track, user=instance.user
        )


@receiver(post_save, sender=Vote)
def on_play_created(sender, instance, created, **kwargs):
    if created:
        Stat.objects.create(
            type='vote', vote=instance, track=instance.track, user=instance.user
        )