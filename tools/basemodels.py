import uuid
from django.db import models
from django.utils import timezone

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from .upload import ModifyUpload


class GenericUUIDModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created = models.DateTimeField('Created date', db_index=True, blank=True, null=True)  # temp
    updated = models.DateTimeField('Updated date', auto_now=True, db_index=True)

    # deleted = models.DateTimeField('Deleted date', blank=True, null=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()
        super(GenericUUIDModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

    # def delete(self):
    #     self.deleted = timezone.now()
    #     self.save()
    #
    # def restore(self):
    #     self.deleted = None
    #     self.save()


class GenericIDModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    created = models.DateTimeField('Created date', db_index=True, blank=True, null=True)  # temp
    updated = models.DateTimeField('Updated date', auto_now=True, db_index=True)

    # deleted = models.DateTimeField('Deleted date', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()
        super(GenericIDModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class GenericIPCatcher(models.Model):
    ip = models.CharField('IP Address', max_length=46, null=True)
    ipv = models.CharField('IP Version', max_length=16, null=True)

    class Meta:
        abstract = True


class S3Image(GenericIDModel):
    s3_source = models.ImageField(upload_to=ModifyUpload('s3_all'), max_length=512, blank=False, null=False)

    # note that we create width and height only for source image
    # all the auto-generated images will have the same proportions (i hope)
    s3_source_width = models.IntegerField(null=True, editable=False)
    s3_source_height = models.IntegerField(null=True, editable=False)

    # auto-generated fields
    # todo maybe refactor this to remove indian code
    # s3_image_1920 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
    #                                processors=[ResizeToFit(width=1920, upscale=False)])
    # s3_image_1280 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
    #                                processors=[ResizeToFit(width=1280, upscale=False)])
    s3_image_960 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                  processors=[ResizeToFit(width=960, upscale=False)])
    s3_image_720 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                  processors=[ResizeToFit(width=720, upscale=False)])
    s3_image_480 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                  processors=[ResizeToFit(width=480, upscale=False)])
    s3_image_320 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                  processors=[ResizeToFit(width=320, upscale=False)])

    # def save(self, *args, **kwargs):
    #     if self.s3_source:
    #         self.s3_source_width = self.s3_source.width
    #         self.s3_source_height = self.s3_source.height
    #     super(S3ImageMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
