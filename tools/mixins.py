from io import BytesIO
import os
from io import StringIO
from django.core.files.base import ContentFile

from rest_framework import serializers
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from tools.upload import ModifyUpload
from PIL import Image
from settings.base import THUMBNAIL_SIZE

from django.core.files.storage import default_storage as storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from tools.geo import GEO_search_coordinates_by_location
from django.utils.text import slugify

from .basemodels import GenericIDModel


class PictureManualThumbnail(models.Model):
    picture_thumbnail = models.FileField(upload_to=ModifyUpload('thumbnail'), null=True, blank=True)

    class Meta:
        abstract = True


class PictureThumbnail(models.Model):

    def generate_thumbnail(self, save=True):

        try:

            if not self.picture or self.picture_thumbnail:
                return

            """
            Create and save the thumbnail for the photo (simple resize with PIL).
            """

            fh = storage.open(self.picture.name, 'rb')
            try:
                image = Image.open(fh)
            except:
                return False
            # image = Image.open(fh)

            image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
            fh.close()

            # Path to save to, name, and extension
            thumb_name, thumb_extension = os.path.splitext(self.picture.name)
            thumb_extension = thumb_extension.lower()

            thumb_filename = thumb_name + '_thumb' + thumb_extension

            if thumb_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif thumb_extension == '.gif':
                FTYPE = 'GIF'
            elif thumb_extension == '.png':
                FTYPE = 'PNG'
            else:
                return False  # Unrecognized file type

            # Save thumbnail to in-memory file as StringIO
            temp_thumb = BytesIO()
            image.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)

            # Load a ContentFile into the thumbnail field so it gets saved
            self.picture_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=save)
            temp_thumb.close()

            # if save:
            #     self.save()

            return True

        except:
            # i don't really care, i have a lot to do
            return False

    class Meta:
        abstract = True


# class PictureThumbnailSerializer(serializers.Serializer):
#     picture_thumbnail_150 = serializers.SerializerMethodField()
#     picture_thumbnail_70 = serializers.SerializerMethodField()
#
#     def get_picture_thumbnail_150(self, obj):
#         if obj.picture_thumbnail_150:
#             return obj.picture_thumbnail_150.url
#         return None
#
#     def get_picture_thumbnail_70(self, obj):
#         if obj.picture_thumbnail_70:
#             return obj.picture_thumbnail_70.url
#         return None
#
#     class Meta:
#         abstract = True


class LocationObjectMixin(models.Model):
    location = models.CharField(max_length=1024, null=True, blank=True,
                                help_text="Free-form query string to search for")
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)

    def process_location(self):
        location = GEO_search_coordinates_by_location(self.location)
        if location and 'lon' in location and 'lat' in location:
            self.location_longitude = float(location['lon'])
            self.location_latitude = float(location['lat'])
            super().save()

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(editable=True, max_length=255, default=None, null=True, blank=True, unique=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(SlugMixin, self).save()

    class Meta:
        abstract = True
