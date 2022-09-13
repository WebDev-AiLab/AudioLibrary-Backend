from django.contrib import admin
from .models import Play, Vote, Comment, TrackPlays, CommentArtists, CommentTracks, Stat
from django.db.models import Count
from related_admin import RelatedFieldAdmin


class StatAdmin(admin.ModelAdmin):
    list_display = ('type', 'track', 'artist', 'user', 'created')
    list_filter = ('type', 'track', 'user')
    readonly_fields = ('created', 'type', 'track', 'user')

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('track', 'user',)
        }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )

    def artist(self, obj):
        return obj.track.original_artist

    artist.admin_order_field = 'track__original_artist'


admin.site.register(Stat, StatAdmin)


# Register your models here.
class PlayAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_artist', 'plays_count',)
    search_fields = ('title', 'original_artist')

    def get_queryset(self, request):
        qs = super(PlayAdmin, self).get_queryset(request)
        return qs.annotate(play_count=Count('plays')).filter(play_count__gte=1)


admin.site.register(TrackPlays, PlayAdmin)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('track', 'user', 'created')
    ordering = ('-created',)

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('track', 'user',)
        }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )


admin.site.register(Vote, VoteAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('track', 'artist', 'user', 'text', 'created')
    ordering = ('-created',)
    list_editable = ('text',)
    readonly_fields = ('track', 'user')
    search_fields = ('user__username', 'track__title', 'artist__name')

    change_list_template = 'admin/comment_list_admin.html'

    def artist(self, obj):
        return obj.track.original_artist

    artist.admin_order_field = 'track__artist'

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('track', 'user', 'text')
        }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )


# admin.site.register(Comment, CommentAdmin)


class CommentArtistAdmin(CommentAdmin):
    list_display = ('artist', '_user', 'text', 'created')

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('artist', 'user', 'text')
        }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )

    def _user(self, obj):
        if obj.user and not obj.user.is_guest:
            return obj.user
        return 'Anonymous'

    _user.admin_order_field = 'user__username'

    def get_queryset(self, request):
        qs = super(CommentArtistAdmin, self).get_queryset(request)
        return qs.filter(track__isnull=True, artist__isnull=False)


# admin.site.register(CommentArtists, CommentArtistAdmin)


class CommentTrackAdmin(CommentAdmin):
    list_display = ('track', '_artist', '_user', 'text', 'created')

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('track', 'user', 'text')
        }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )

    def _user(self, obj):
        if obj.user and not obj.user.is_guest:
            return obj.user
        return 'Anonymous'

    _user.admin_order_field = 'user__username'

    def get_queryset(self, request):
        qs = super(CommentTrackAdmin, self).get_queryset(request)
        return qs.filter(artist__isnull=True, track__isnull=False)

    def _artist(self, obj):
        return obj.track.original_artist

    _artist.admin_order_field = 'track__original_artist'


# admin.site.register(CommentTracks, CommentTrackAdmin)
