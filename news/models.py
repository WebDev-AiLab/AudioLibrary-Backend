from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.
from accounts.models import User
from tools.basemodels import GenericUUIDModel
from tools.mixins import SlugMixin, PictureThumbnail
from tools.upload import ModifyUpload


class Post(GenericUUIDModel, SlugMixin, PictureThumbnail):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    excerpt = models.TextField(null=True, blank=True)

    picture = models.FileField(upload_to=ModifyUpload('post'), null=True, blank=True)
    picture_thumbnail = models.FileField(upload_to=ModifyUpload('post_thumbnail'), null=True, blank=True)

    def __str__(self):
        return self.title
