from django.contrib import admin
from interactions.models import Comment


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ('type', '_subject', '_user', 'text', 'created')
    list_filter = ('type', 'user',)

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('type', 'track', 'artist', 'user',)
        }),
        ('CONTENT', {
            'fields': ('text',)
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

    def _artist(self, obj):
        if obj.track:
            return obj.track.original_artist
        return None

    _artist.admin_order_field = 'track__original_artist'

    def _subject(self, obj):
        if obj.track:
            return obj.track.original_artist
        if obj.artist:
            return obj.artist.name
        return None


admin.site.register(Comment, CommentAdmin)
