from django.db import models
from tracks.models import Track, Artist


class UploadTrack(Track):
    class Meta:
        proxy = True
        verbose_name = "Upload Tracks"
        verbose_name_plural = verbose_name


class UploadArtists(Artist):
    class Meta:
        proxy = True
        verbose_name = "Upload Artists"
        verbose_name_plural = verbose_name
