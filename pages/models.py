from django.db import models
from tools.basemodels import GenericUUIDModel, GenericIDModel
from tools.mixins import SlugMixin, PictureThumbnail
from tools.exceptions import WebsiteOperationException
# from tinymce.models import HTMLField
from accounts.models import User
from tools.upload import ModifyUpload

from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Page(GenericIDModel, SlugMixin):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField(null=True, blank=True)

    # this can only be set manually (see scripts/generate_initial_data.py)
    is_deletable = models.BooleanField(default=True, editable=False)
    page_max_width = models.IntegerField(default=1200, help_text='In pixels. Set to 0 to disable limit.')

    url_mask = models.CharField('URL', max_length=1024, unique=True, help_text='Note: URL should contain one leading slash and no trailing slashes')

    TYPE_CHOICES = (
        ('Text', 'Custom Text Page'),
        ('Frontend', 'Frontend Page'),
        ('Mixed', 'Mixed Page'),
    )
    type = models.CharField(max_length=16, db_index=True, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0])

    SECTION_CHOICES = (
        ('Main', 'Main'),
        ('User', 'User'),
    )
    section = models.CharField(max_length=16, choices=SECTION_CHOICES, db_index=True, null=True, blank=True)

    PAGE_CHOICES = (
        # general
        ('HOME', 'Home'),
        ('ARTISTS', 'Artists'),
        ('ARTIST_SINGLE', 'Artist Detail'),
        ('LABELS', 'Labels'),
        ('LABEL_SINGLE', 'Label Detail'),
        ('TRACKS', 'Tracks'),
        ('TRACK_SINGLE', 'Track Detail'),

        # user-related
        ('FAVOURITES', 'User\'s Favorites'),
        ('HISTORY', 'User\'s History'),

        # news
        ('NEWS', 'News Detail'),

        # offer
        ('SUBMIT', 'Offer Track'),

        ('UPLOAD', 'Upload Files')
    )
    page = models.CharField(max_length=64, choices=PAGE_CHOICES, db_index=True, null=True, blank=True)

    order = models.PositiveIntegerField(default=0, null=False, blank=False, db_index=True)

    def delete(self, using=None, keep_parents=False):
        if not self.is_deletable:
            raise WebsiteOperationException('This page is non-deletable, which means that it cannot be deleted.')

        super(Page, self).delete()

    def save(self, *args, **kwargs):
        # add leading slash
        if self.url_mask[0] != '/':
            self.url_mask = f"/{self.url_mask}"

        # remove trailing slash as well
        self.url_mask = self.url_mask.rstrip("/")

        # remove all whitespaces
        self.url_mask = self.url_mask.replace(" ", "")
        super(Page, self).save(*args, **kwargs)

    # def __str__(self):
    #     return self.title

    class Meta:
        ordering = ['order']


class PageMain(Page):
    class Meta:
        proxy = True
        verbose_name = 'Menu Item/Main'
        verbose_name_plural = 'Menu Items/Main'

    def save(self, *args, **kwargs):
        self.section = 'Main'
        super(PageMain, self).save(*args, **kwargs)


class PageUser(Page):
    class Meta:
        proxy = True
        verbose_name = 'Menu Item/User'
        verbose_name_plural = 'Menu Items/User'

    def save(self, *args, **kwargs):
        self.section = 'User'
        super(PageUser, self).save(*args, **kwargs)
