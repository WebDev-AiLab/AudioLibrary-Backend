from django.contrib import admin
from .models import Track, Artist, Album, Label, Genre, Style, ArtistImage, Submission, Rating, ArtistSite, LabelSite, \
    ArtistSocial, ArtistMedia, ArtistYoutube, ArtistAlias, LabelYoutube, LabelMedia, LabelSocial
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, InlineModelAdmin
from django.utils.html import format_html
from django.contrib import admin
from django import forms
from django.db import models
# from images.models import S3Image
# from django_select2 import forms as s2forms

from django.utils.html import escape
from django.utils.safestring import mark_safe

from treebeard.forms import movenodeform_factory
from treebeard.admin import TreeAdmin

from tools.string import generate_random_string

admin.autodiscover()
admin.site.enable_nav_sidebar = False

import time


# class ArtistWidget(s2forms.ModelSelect2MultipleWidget):
#     search_fields = [
#         "name__icontains"
#     ]


class TrackStyleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrackStyleForm, self).__init__(*args, **kwargs)
        self.fields['style'].choices = self._find_style_choices()
        # if self.instance.genre:
        #     self.fields['style'].queryset = Style.objects.filter(genre=self.instance.genre)

    def _find_style_choices(self):
        options = [(None, '---------')]
        queryset = Style.objects.filter(genre=self.instance.genre)
        for option in queryset:
            options.append((option.id, option.name))
        return options


class TrackGenreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrackGenreForm, self).__init__(*args, **kwargs)
        # self.fields['genre'].choices = self._make_dropdown_tree(Genre, for_node=None)

    # class Meta:
    #     widgets = {
    #         'artist': ArtistWidget
    #     }

    # @staticmethod
    # def is_loop_safe(for_node, possible_parent):
    #     if for_node is not None:
    #         return not (
    #                 possible_parent == for_node
    #         ) or (possible_parent.is_descendant_of(for_node))
    #     return True
    #
    # def mk_indent(self, level):
    #     return '&nbsp;&nbsp;&nbsp;&nbsp;' * (level - 1)
    #
    # def add_subtree(self, for_node, node, options):
    #     """ Recursively build options tree. """
    #     if self.is_loop_safe(for_node, node):
    #         for item, _ in node.get_annotated_list(node):
    #             options.append((item.pk, mark_safe(self.mk_indent(item.get_depth()) + escape(item))))
    #
    # def _make_dropdown_tree(self, model, for_node=None):
    #     options = [(None, '---------')]
    #     for node in model.get_root_nodes():
    #         self.add_subtree(for_node, node, options)
    #     return options


class TrackInlineAdmin(NestedStackedInline):
    model = Track
    extra = 0
    # fk_name = 'artist'
    list_display = ('id', 'artist', 'title', 'albub', 'label', 'year', 'celery_upload_status')

    def get_max_num(self, request, obj=None, **kwargs):
        return 1


class TrackAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'original_artist', 'album', 'label', 'style', 'type', 'BPM', 'rating', 'year', 'length',
        'plays_count', 'votes_count', 'show_new_releases', 'created')
    readonly_fields = ('celery_upload_status', 'plays_count', 'votes_count')
    ordering = ('-created', 'original_artist',)
    list_filter = ('artist', 'album', 'style', 'label', 'celery_upload_status')
    search_fields = ('artist__name', 'title', 'original_artist', 'album', 'label__name', 'style__name')
    autocomplete_fields = ['artist', 'label']
    list_editable = ('show_new_releases',)

    save_on_top = True

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': (
                'slug', 'original_file_name', 'title', 'original_artist', 'album', 'type', 'rating', 'duration', 'BPM',
                'year',)
        }),
        ('RELATIONS WITH OTHER TABLES', {
            'fields': ('artist', 'style', 'label',)
        }),
        ('MEDIA', {
            'fields': ('file', 'waveform', 'picture', 'picture_thumbnail',)
        }),
        ('OTHER', {
            'fields': ('lyrics',)
        }),
        ('ACCOUNTS', {
            'fields': ('plays_count', 'votes_count')
        }),
        ('SYSTEM', {
            'fields': ('celery_upload_status',)
        }),
    )

    form = TrackStyleForm

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     ff db_field.name == ""

    class Media:
        js = (
            '/media/js/admin-track-style-select.js',
            '/media/js/admin-track-delete-plays.js'
        )
        css = {
            'screen': ('/media/css/custom.admin.css?nocache=' + generate_random_string(6),)
        }

    def parsed_artist(self, obj):
        return ", ".join([p.name for p in obj.artist.all()]) or obj.original_artist or obj.original_file_name

    def length(self, obj):
        return time.strftime('%M:%S', time.gmtime(obj.duration))

    # def _title(self, obj):
    #     return obj.title if obj.title else obj.original_file_name


admin.site.register(Track, TrackAdmin)


class S3ImageInlineArtistAdmin(admin.TabularInline):
    model = ArtistImage
    extra = 0
    list_display = ('source',)
    fields = ('s3_source',)


class LabelSiteInline(admin.TabularInline):
    model = LabelSite
    extra = 0
    list_display = ('url',)
    fields = ('url',)


class LabelYoutubeInline(admin.TabularInline):
    model = LabelYoutube
    extra = 0
    list_display = ('url',)
    fields = ('url',)


class LabelMediaInline(admin.TabularInline):
    model = LabelMedia
    extra = 0
    list_display = ('source', 'url')
    fields = ('source', 'url')


class LabelSocialInline(admin.TabularInline):
    model = LabelSocial
    extra = 0
    list_display = ('source', 'url')
    fields = ('source', 'url')


class ArtistYoutubeInline(admin.TabularInline):
    model = ArtistYoutube
    extra = 0
    list_display = ('url',)
    fields = ('url',)


class ArtistMediaInline(admin.TabularInline):
    model = ArtistMedia
    extra = 0
    list_display = ('source', 'url')
    fields = ('source', 'url')


class ArtistSocialInline(admin.TabularInline):
    model = ArtistSocial
    extra = 0
    list_display = ('source', 'url')
    fields = ('source', 'url')


class ArtistSiteInline(admin.TabularInline):
    model = ArtistSite
    extra = 0
    list_display = ('url',)
    fields = ('url',)


class ArtistAliasesInline(admin.TabularInline):
    model = ArtistAlias
    extra = 0
    list_display = ('alias',)
    fields = ('alias',)


class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'real_name', 'birthday', 'birth_location', 'location', 'aliases', 'social', 'websites', 'wikipedia', 'youtube', '_media', 'discogs', 'beatport', 'contact_info',
        'status', 'singer', 'voice_type', '_tracks', 'visible')
    ordering = ('name',)
    search_fields = ('name', 'slug', 'artist_aliases__alias')
    list_editable = ('visible',)

    save_on_top = True

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('visible', 'name', 'real_name', 'bio', 'birthday', 'birth_location', 'contact_info', 'is_wikipedia', 'wikipedia', 'discogs', 'beatport', 'status', 'singer', 'voice_type', 'is_daw', 'daw')
        }),
        ('MEDIA', {
            'fields': ('picture', 'picture_thumbnail',)
        }),
        ('LOCATION', {
            'fields': ('location', 'location_latitude', 'location_longitude',)
        }),
        # ('ABOUT', {
        #     'fields': (
        #     'real_name', 'profile_aliases', 'bio', 'birthday', 'location', 'birth_location', 'type', 'voice_type')
        # }),
        # ('SYSTEM', {
        #     'fields': ('created',)
        # }),
    )

    def websites(self, obj):
        if not obj.artist_sites.count():
            return None

        string = ''
        for idx, link in enumerate(ArtistSite.objects.filter(artist=obj)):
            string += f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{link.url}'>{link.url}</a><br/>"
        return format_html(string)

    def social(self, obj):
        if not obj.artist_social.count():
            return None

        string = ''
        for idx, link in enumerate(ArtistSocial.objects.filter(artist=obj)):
            string += f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{link.url}'>{link.source}: {link.url}</a><br/>"
        return format_html(string)

    def youtube(self, obj):
        if not obj.artist_youtubes.count():
            return None

        string = ''
        for idx, link in enumerate(ArtistYoutube.objects.filter(artist=obj)):
            string += f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{link.url}'>{link.url}</a><br/>"
        return format_html(string)

    def _media(self, obj):
        if not obj.artist_medias.count():
            return None

        string = ''
        for idx, link in enumerate(ArtistMedia.objects.filter(artist=obj)):
            string += f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{link.url}'>{link.source}: {link.url}</a><br/>"
        return format_html(string)

    def aliases(self, obj):
        if not obj.artist_aliases.count():
            return None

        string = ''
        for alias in ArtistAlias.objects.filter(artist=obj):
            string += f"{alias.alias}, "

        return string[:-2]

    class Media:
        css = {
            'screen': ('/media/css/custom.admin.css', '/media/css/custom.admin.label.css')
        }
        js = (
            '/media/js/admin-artist-content.js?nocache=555',
        )

    inlines = [ArtistAliasesInline, ArtistSocialInline, ArtistSiteInline, ArtistYoutubeInline, ArtistMediaInline,
               S3ImageInlineArtistAdmin]

    def get_queryset(self, request):
        qs = super(ArtistAdmin, self).get_queryset(request)
        return qs.annotate(models.Count('tracks'))

    def _tracks(self, obj):
        url = f"/admin/tracks/track/?artist__id__exact={obj.id}"
        return format_html("<a href='{}'>{}</a>", url, obj.tracks.count())
    _tracks.admin_order_field = 'tracks__count'


admin.site.register(Artist, ArtistAdmin)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'parsed_artist', 'tracks_count', 'tracks_link', 'created')
    ordering = ('-created',)
    search_fields = ('title', 'artist__name')
    form = TrackGenreForm

    autocomplete_fields = ['artist']
    save_on_top = True

    # inlines = [TrackInlineAdmin]

    fieldsets = (
        ('GENERAL INFORMATION (FROM .MP3 TAG)', {
            'fields': ('title', 'album_artist', 'year')
        }),
        ('RELATIONS', {
            'fields': ('artist', 'genre')
        }),
        ('MEDIA', {
            'fields': ('picture', 'picture_thumbnail',)
        })
    )

    class Media:
        css = {
            'screen': ('/media/css/custom.admin.css',)
        }

    def tracks_link(self, obj):
        url = f"/admin/tracks/track/?album__iexact={obj.title}"
        return format_html("<a href='{}'>See tracks</a>", url)


admin.site.register(Album, AlbumAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'tracks_count', 'tracks_link', 'created')
    # ordering = ('-created',)
    search_fields = ('name',)
    # inlines = [TrackInlineAdmin]
    # form = movenodeform_factory(Genre)

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('name',)
        }),
        ('MEDIA', {
            'fields': ('picture', 'picture_thumbnail',)
        }),
        # ('SYSTEM', {
        #     'fields': ('created',)
        # }),
    )

    def tracks_link(self, obj):
        url = f"/admin/tracks/track/?genre__id__exact={obj.id}"
        return format_html("<a href='{}'>See tracks</a>", url)


# admin.site.register(Genre, GenreAdmin)


class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'social', 'websites', 'youtube', '_media', 'discogs', 'beatport', 'sublabel', '_tracks')
    ordering = ('-created',)
    search_fields = ('name',)
    # list_filter = ('country',)

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('name', 'description', 'contact_info', 'discogs', 'beatport')
        }),
        ('MEDIA', {
            'fields': ('picture', 'picture_thumbnail',)
        }),
        ('RELATIONS', {
            'fields': ('sublabel',)
        }),
        # ('ABOUT', {
        #     'fields': ('description', 'country', 'founded', 'contact_info')
        # }),
        # ('SYSTEM', {
        #     'fields': ('created',)
        # }),
    )

    class Media:
        css = {
            'screen': ('/media/css/custom.admin.css', '/media/css/custom.admin.label.css'),
        }

    inlines = [LabelSocialInline, LabelSiteInline, LabelYoutubeInline, LabelMediaInline]

    def websites(self, obj):
        if not obj.label_sites.count():
            return None

        string = ''
        for idx, link in enumerate(LabelSite.objects.filter(label=obj)):
            string += f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{link.url}'>{link.url}</a><br/>"
        return format_html(string)

    def social(self, obj):
        if not obj.label_social.count():
            return None

        string = ''
        for idx, link in enumerate(LabelSocial.objects.filter(label=obj)):
            string += f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{link.url}'>{link.source}: {link.url}</a><br/>"
        return format_html(string)

    def youtube(self, obj):
        if not obj.label_youtubes.count():
            return None

        string = ''
        for idx, link in enumerate(LabelYoutube.objects.filter(label=obj)):
            string += f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{link.url}'>{link.url}</a><br/>"
        return format_html(string)

    def _media(self, obj):
        if not obj.label_medias.count():
            return None

        string = ''
        for idx, link in enumerate(LabelMedia.objects.filter(label=obj)):
            string += f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{link.url}'>{link.source}: {link.url}</a><br/>"
        return format_html(string)

    def get_queryset(self, request):
        qs = super(LabelAdmin, self).get_queryset(request)
        return qs.annotate(models.Count('tracks'))

    def _tracks(self, obj):
        url = f"/admin/tracks/track/?label__id__exact={obj.id}"
        return format_html("<a href='{}'>{}</a>", url, obj.tracks.count())

    _tracks.admin_order_field = 'tracks__count'

admin.site.register(Label, LabelAdmin)


class StyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default', 'tracks_count', 'tracks_link',)
    ordering = ('name',)
    search_fields = ('name',)
    # autocomplete_fields = ('genre',)
    list_editable = ('is_default',)

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('name', 'is_default', 'description')
        }),
        ('MEDIA', {
            'fields': ('picture', 'picture_thumbnail',)
        }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )

    def tracks_link(self, obj):
        url = f"/admin/tracks/track/?style__id__exact={obj.id}"
        return format_html("<a href='{}'>See tracks</a>", url)

    def genres(self, obj):
        return ", ".join([p.name for p in obj.genre.all()])

    class Media:
        css = {
            'screen': ('/media/css/custom.admin.css',)
        }


admin.site.register(Style, StyleAdmin)


# class SubmissionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'name', 'user', 'email', 'created')
#     ordering = ('-created',)
#     search_fields = ('title', 'name',)
#     readonly_fields = ('file', 'title', 'name', 'user', 'email')
#
#     fieldsets = (
#         ('GENERAL INFORMATION', {
#             'fields': ('file', 'title', 'name', 'user', 'email')
#         }),
#         # ('MEDIA', {
#         #     'fields': ('picture', 'picture_thumbnail',)
#         # }),
#         ('SYSTEM', {
#             'fields': ('created',)
#         }),
#     )
#
#
# admin.site.register(Submission, SubmissionAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating', 'created')
    ordering = ('-rating',)
    search_fields = ('rating',)

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('rating', 'description',)
        }),
        # ('MEDIA', {
        #     'fields': ('picture', 'picture_thumbnail',)
        # }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )

# admin.site.register(Rating, RatingAdmin)
