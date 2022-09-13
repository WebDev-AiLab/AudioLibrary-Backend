from django.db import models
from tools.upload import ModifyUpload
from tools.basemodels import GenericIDModel

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class S3Image(GenericIDModel):
    s3_source = models.ImageField(upload_to=ModifyUpload('s3_all'), max_length=512, blank=True, null=True)

    # note that we create width and height only for source image
    # all the auto-generated images will have the same proportions (i hope)
    s3_source_width = models.IntegerField(null=True, editable=False)
    s3_source_height = models.IntegerField(null=True, editable=False)

    # auto-generated fields
    # todo maybe refactor this to remove indian code
    s3_image_1920 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                   processors=[ResizeToFit(width=1920, upscale=False)])
    s3_image_1280 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                   processors=[ResizeToFit(width=1280, upscale=False)])
    s3_image_960 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                  processors=[ResizeToFit(width=960, upscale=False)])
    s3_image_720 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                  processors=[ResizeToFit(width=720, upscale=False)])
    s3_image_480 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                  processors=[ResizeToFit(width=480, upscale=False)])
    s3_image_320 = ImageSpecField(source='s3_source', format='WEBP', options={'quality': 80},
                                  processors=[ResizeToFit(width=320, upscale=False)])

    def save(self, *args, **kwargs):
        if self.s3_source:
            self.s3_source_width = self.s3_source.width
            self.s3_source_height = self.s3_source.height
        super(S3Image, self).save(*args, **kwargs)
