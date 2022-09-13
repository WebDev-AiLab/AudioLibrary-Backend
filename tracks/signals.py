from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Track, Album, Artist, Label, Genre, Style, Submission
from .utils import process_track, parse_links, create_search_vectors


@receiver(post_save, sender=Track)
def on_track_save(sender, instance, created, **kwargs):
    instance.generate_thumbnail(save=True)
    if created:
        process_track(instance)

    # should be done every time fields change
    # or just every time
    create_search_vectors(instance)


@receiver(post_save, sender=Album)
def on_album_save(sender, instance, created, **kwargs):
    instance.generate_thumbnail(save=True)


@receiver(post_save, sender=Artist)
def on_artist_save(sender, instance, created, **kwargs):
    instance.generate_thumbnail(save=True)

    # the function in the mixin runs even if everything is already fill (to update for example), so we have to check it
    if instance.location and not (instance.location_latitude and instance.location_longitude):
        instance.process_location()


@receiver(post_save, sender=Label)
def on_label_save(sender, instance, created, **kwargs):
    instance.generate_thumbnail(save=True)


@receiver(post_save, sender=Genre)
def on_genre_save(sender, instance, created, **kwargs):
    instance.generate_thumbnail(save=True)


@receiver(post_save, sender=Style)
def on_style_save(sender, instance, created, **kwargs):
    instance.generate_thumbnail(save=True)


@receiver(post_save, sender=Submission)
def on_submission_save(sender, instance, created, **kwargs):
    # let's find all links in the text
    if created:
        parse_links(instance)
