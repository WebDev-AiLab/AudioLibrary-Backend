from django.db import models
from tools.basemodels import GenericIDModel, GenericUUIDModel, GenericIPCatcher
from tracks.models import Track, Artist
# from accounts.models import Guest
from django.conf import settings


# class Interaction(GenericUUIDModel, GenericIPCatcher):
#     track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='interactions')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='likes')


class Play(GenericIDModel, GenericIPCatcher):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='plays')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Play, self).save()
        self.track.evaluate_counts()

    def delete(self, using=None, keep_parents=False):
        super(Play, self).delete()
        self.track.evaluate_counts()


class Vote(GenericIDModel):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='likes')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Vote, self).save()
        self.track.evaluate_counts()

    def delete(self, using=None, keep_parents=False):
        super(Vote, self).delete()
        self.track.evaluate_counts()


class Comment(GenericUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(max_length=2048)

    at = models.IntegerField('Created At', default=0)

    TYPE_CHOICES = (
        ('track', 'Track'),
        ('artist', 'Artist')
    )
    type = models.CharField(max_length=16, db_index=True, choices=TYPE_CHOICES)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)


class TrackPlays(Track):
    class Meta:
        proxy = True
        verbose_name = 'Play'
        verbose_name_plural = 'Plays'


class CommentArtists(Comment):
    class Meta:
        proxy = True
        verbose_name = 'Comment/Artist'
        verbose_name_plural = 'Comments/Artist'

    def save(self, *args, **kwargs):
        self.track = None
        super(CommentArtists, self).save(*args, **kwargs)


class CommentTracks(Comment):
    class Meta:
        proxy = True
        verbose_name = 'Comment/Track'
        verbose_name_plural = 'Comments/Track'

    def save(self, *args, **kwargs):
        self.artist = None
        super(CommentTracks, self).save(*args, **kwargs)


# temporary
# todo create a single model for interactions and then proxies for likes/votes
class Stat(GenericIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('vote', 'Like'),
        ('play', 'Play')
    )
    type = models.CharField(max_length=16, db_index=True, choices=TYPE_CHOICES)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, null=True, blank=True)
    play = models.ForeignKey(Play, on_delete=models.CASCADE, null=True, blank=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
