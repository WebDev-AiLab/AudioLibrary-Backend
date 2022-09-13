from django.db import models
from tools.basemodels import GenericUUIDModel, S3Image
# from tools.mixins import S3ImageMixin
from tools.upload import ModifyUpload
from treebeard.ns_tree import NS_Node
from django.utils.text import slugify
from tools.mixins import PictureThumbnail, LocationObjectMixin
# from images.models import S3Image
from accounts.models import User
from django.utils.html import mark_safe
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class Artist(GenericUUIDModel, PictureThumbnail, LocationObjectMixin):
    slug = models.SlugField(editable=False, max_length=255, default=None, null=True, unique=True)
    name = models.CharField('Artist Name', max_length=512, unique=True)
    # excerpt = models.CharField('Artist Info', max_length=128, help_text='Very short line containing essential information about artist, for instance \'British Rock-Band\'; It will be displayed right below the artist name.', null=True, blank=True)

    picture = models.FileField(upload_to=ModifyUpload('artist'), null=True, blank=True)
    picture_thumbnail = models.FileField(upload_to=ModifyUpload('thumbnail'), null=True, blank=True)

    bio = models.TextField('Profile', null=True, blank=True)

    birthday = models.DateField('Date of birth', null=True, blank=True)
    birth_location = models.CharField('Place of birth', max_length=1024, null=True, blank=True)
    location = models.CharField('Place of living', max_length=1024, null=True, blank=True)

    real_name = models.CharField(max_length=255, null=True, blank=True)
    # profile_aliases = models.TextField(null=True, blank=True, help_text='Write every entity from a new line')

    # TYPE_CHOICES = (
    #     ('Composer', 'Composer'),
    #     ('Singer', 'Singer')
    # )
    # type = models.CharField(choices=TYPE_CHOICES, max_length=32, null=True, blank=True)
    singer = models.BooleanField(default=False)
    voice_type = models.CharField('Type of Voice', max_length=64, null=True, blank=True)

    # only for my own purposes, delete it if you don't need it
    hide = models.BooleanField('Hide', default=False, db_index=True, help_text='Temporary field, i will remove it very soon')

    # and this is for production
    visible = models.BooleanField('Visible', default=True, db_index=True)

    contact_info = models.EmailField('Contact Info', null=True, blank=True)

    # sites
    is_wikipedia = models.BooleanField('Has Wikipedia page', default=False)
    wikipedia = models.URLField(null=True, blank=True)

    # other
    is_daw = models.BooleanField('DAW', default=False)
    daw = models.CharField('DAW', max_length=255, null=True, blank=True)

    # other
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    )
    status = models.CharField(null=True, blank=True, max_length=16, choices=STATUS_CHOICES)

    # social
    discogs = models.URLField(null=True, blank=True, db_index=True)
    beatport = models.URLField(null=True, blank=True, db_index=True)

    # images = models.ManyToManyField(S3Image, related_name='artists')

    @property
    def tracks_count(self, ):
        return self.tracks.count()

    # ... maybe some other info

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

        super(Artist, self).save()


class ArtistSite(GenericUUIDModel):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_sites')
    url = models.URLField()


class ArtistAlias(GenericUUIDModel):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_aliases')
    alias = models.CharField(max_length=255, db_index=True)


class ArtistYoutube(GenericUUIDModel):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_youtubes')
    # SITE_CHOICES = (
    #     ('Spotify', 'Spotify'),
    #     ('Apple Music', 'Apple Music'),
    # )
    # service = models.CharField(choices=SITE_CHOICES, max_length=64, db_index=True)
    url = models.URLField()

    class Meta:
        verbose_name = "YouTube link"
        verbose_name_plural = "YouTube links"


class ArtistMedia(GenericUUIDModel):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_medias')
    SITE_CHOICES = (
        ('Spotify', 'Spotify'),
        ('Apple Music', 'Apple Music'),
    )
    source = models.CharField('Service', choices=SITE_CHOICES, max_length=64, db_index=True)
    url = models.URLField()


class ArtistSocial(GenericUUIDModel):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artist_social')
    SITE_CHOICES = (
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
        ('VK', 'VK'),
    )
    source = models.CharField('Social Network', choices=SITE_CHOICES, max_length=64, db_index=True)
    url = models.URLField()


class ArtistImage(S3Image):
    artist = models.ForeignKey(Artist, related_name='artist_images', on_delete=models.CASCADE)


class Genre(GenericUUIDModel, PictureThumbnail):
    name = models.CharField('Genre', max_length=512, unique=True)
    picture = models.FileField(upload_to=ModifyUpload('genre'), null=True, blank=True)
    picture_thumbnail = models.FileField(upload_to=ModifyUpload('thumbnail'), null=True, blank=True)
    # is_default = models.BooleanField(default=False, db_index=True, help_text='Means that this genre will be selected by default if there is nothing in the tags')

    node_order_by = ['name']

    def __str__(self):
        return "{}".format(self.name)

    @property
    def tracks_count(self, ):
        return self.tracks.count()

    def save(self, *args, **kwargs):
        # remove all the defaults, and set new
        # if self.is_default:
        #     Genre.objects.filter(is_default=True).update(is_default=False)
        super(Genre, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # self._resize()
        super(Genre, self).save()


class Label(GenericUUIDModel, PictureThumbnail):
    name = models.CharField('Label name', max_length=512, unique=True)
    picture = models.FileField(upload_to=ModifyUpload('label'), null=True, blank=True)
    picture_thumbnail = models.FileField(upload_to=ModifyUpload('thumbnail'), null=True, blank=True)

    description = models.TextField('Profile', null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=255)
    founded = models.IntegerField('Year Founded', null=True, blank=True)

    contact_info = models.EmailField('Contact Info', null=True, blank=True)

    slug = models.SlugField(editable=False, max_length=255, default=None, null=True, unique=True)

    # social
    discogs = models.URLField(null=True, blank=True, db_index=True)
    beatport = models.URLField(null=True, blank=True, db_index=True)

    sublabel = models.ForeignKey("self", on_delete=models.SET_NULL, help_text="Set SubLabel from current table", blank=True, null=True)
    # sublabel_string = models.CharField(max_length=255, blank=True, null=True, help_text="Set SubLabel from string",)

    def __str__(self):
        return "{}".format(self.name)

    @property
    def tracks_count(self, ):
        return self.tracks.count()

    def save(self, *args, **kwargs):
        # self._resize()
        self.slug = slugify(self.name, allow_unicode=True)
        super(Label, self).save()


class LabelSite(GenericUUIDModel):
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='label_sites')
    url = models.URLField()

    # order = models.PositiveIntegerField(default=0, blank=False, null=False)
    #
    # class Meta:
    #     ordering = ['order']


class LabelYoutube(GenericUUIDModel):
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='label_youtubes')
    # SITE_CHOICES = (
    #     ('Spotify', 'Spotify'),
    #     ('Apple Music', 'Apple Music'),
    # )
    # service = models.CharField(choices=SITE_CHOICES, max_length=64, db_index=True)
    url = models.URLField()

    class Meta:
        verbose_name = "YouTube link"
        verbose_name_plural = "YouTube links"


class LabelMedia(GenericUUIDModel):
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='label_medias')
    SITE_CHOICES = (
        ('Spotify', 'Spotify'),
        ('Apple Music', 'Apple Music'),
    )
    source = models.CharField('Service', choices=SITE_CHOICES, max_length=64, db_index=True)
    url = models.URLField()


class LabelSocial(GenericUUIDModel):
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='label_social')
    SITE_CHOICES = (
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
        ('VK', 'VK'),
    )
    source = models.CharField('Social Network', choices=SITE_CHOICES, max_length=64, db_index=True)
    url = models.URLField()


class Album(GenericUUIDModel, PictureThumbnail):
    title = models.CharField('Album title', max_length=512, unique=True)
    original_artist = models.CharField(max_length=1024, null=True, blank=True)
    album_artist = models.CharField(max_length=1024, null=True, blank=True)
    artist = models.ManyToManyField(Artist, related_name='albumd')
    picture = models.FileField(upload_to=ModifyUpload('album'), null=True, blank=True)
    picture_thumbnail = models.FileField(upload_to=ModifyUpload('thumbnail'), null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.parsed_artist} - {self.title}"

    @property
    def tracks_count(self):
        return Track.objects.filter(album__iexact=self.title).count()

    @property
    def parsed_artist(self):
        return ", ".join([p.name for p in self.artist.all()]) or ""

    def save(self, *args, **kwargs):
        # self._resize()
        super(Album, self).save()


class Style(GenericUUIDModel, PictureThumbnail):
    name = models.CharField(max_length=255)
    # genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    picture = models.ImageField(upload_to=ModifyUpload('style'), null=True, blank=True)
    picture_thumbnail = models.FileField(upload_to=ModifyUpload('thumbnail'), null=True, blank=True)

    description = models.CharField(max_length=2048, null=True, blank=True)
    genre = models.ManyToManyField(Genre)

    @property
    def tracks_count(self, ):
        return self.tracks.count()

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        # only one style can be selected by default
        if self.is_default:
            Style.objects.filter(is_default=True).update(is_default=False)
        super(Style, self).save(*args, **kwargs)


class Track(GenericUUIDModel, PictureThumbnail):
    slug = models.SlugField(editable=True, max_length=255, default=None, null=True, unique=True,
                            help_text='Part of the URL on the main Track page. Must me unique.')
    original_file_name = models.CharField(default='track.mp3', max_length=2048)
    file = models.FileField('.MP3 File', upload_to=ModifyUpload('file'), help_text='.mp3 file location')
    waveform = models.FileField(upload_to=ModifyUpload('waveform'), help_text='Link to file with waveform data')
    picture = models.ImageField(upload_to=ModifyUpload('track'))
    picture_thumbnail = models.FileField(upload_to=ModifyUpload('thumbnail'), null=True, blank=True)

    # meta
    title = models.CharField('Track title', max_length=2048, null=True, blank=True, db_index=True)
    artist = models.ManyToManyField(Artist, verbose_name='Artist list', related_name='tracks',
                                    help_text='Parsed artists from "Compositor" tag or filename.')
    original_artist = models.CharField('Artist', max_length=1024, null=True, blank=True,
                                       help_text='Contains artist field from .mp3 tag', db_index=True)
    # album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    album = models.CharField(null=True, blank=True, max_length=1024, db_index=True)
    album_artist = models.CharField(null=True, blank=True, max_length=1024)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')

    TYPE_CHOICES = [
        ('Vocal', 'Vocal'),
        ('Non-Vocal', 'Non-Vocal')
    ]
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], db_index=True)
    BPM = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    duration = models.FloatField('Length', null=True, help_text='Retrieved track duration in seconds')

    rating = models.CharField('Class', max_length=5, null=True, blank=True)
    remixes = models.CharField(max_length=255, null=True, blank=True)

    lyrics = models.TextField(null=True, blank=True)

    CELERY_UPLOAD_STATUS_CHOICES = (
        (0, 'PENDING'),
        (1, 'PROCESSING'),
        (2, 'FAILED'),
        (3, 'SUCCESS')
    )
    celery_upload_status = models.IntegerField('Celery upload status', choices=CELERY_UPLOAD_STATUS_CHOICES,
                                               default=CELERY_UPLOAD_STATUS_CHOICES[0][0], editable=True, db_index=True,
                                               help_text='Processing status. All tracks are processed in the background after upload. If everything is successful, then the status will be "success", if not - "failed". This field is filled during processing and cannot be changed manually.')

    # data
    plays_count = models.IntegerField(default=0, editable=False, verbose_name='Plays')
    votes_count = models.IntegerField(default=0, editable=False, verbose_name='Likes')

    show_new_releases = models.BooleanField(default=0)

    # search stuff
    title_search_vector = SearchVectorField(null=True, editable=False)
    original_artist_search_vector = SearchVectorField(null=True, editable=False)

    # temp todo save it in database like plays and voteds

    class Meta:
        indexes = [GinIndex(fields=["title_search_vector"]), GinIndex(fields=["original_artist_search_vector"])]

    @property
    def comments_count(self):
        return self.comments.count()

    def _plays_count(self):
        return self.plays.count()

    def _votes_count(self):
        return self.votes.count()

    def evaluate_counts(self):
        self.plays_count = self._plays_count()
        self.votes_count = self._votes_count()

        self.save()

    def set_slug(self):
        if not self.title:
            self.slug = str(self.id)
        else:
            self.slug = "-".join([slugify(self.title, allow_unicode=True), str(self.id)])

    def __str__(self):
        return "{}".format(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.set_slug()

        # generate thumbnails
        # self._resize()
        super(Track, self).save(*args, **kwargs)


class Submission(GenericUUIDModel):
    # file = models.FileField('.MP3 File', upload_to=ModifyUpload('file'), help_text='.mp3 file location', editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # email = models.EmailField(max_length=512, null=True)
    # title = models.CharField(max_length=2048)
    # name = models.CharField(max_length=2048)
    text = models.TextField('Raw Text', null=True, blank=True)

    # @property
    # def file_download(self):
    #     if self.file:
    #         return mark_safe('<a href="{0}" download>Click Here to Download</a>'.format(
    #             self.file.url))
    #     return None


class Rating(GenericUUIDModel):
    rating = models.CharField(max_length=16)
    description = models.TextField(null=True, blank=True)

