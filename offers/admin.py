from django.contrib import admin
from django.utils.html import format_html
from tools.youtube import get_yt_video_id

from .models import Offer, OfferLink


class OfferLinkInline(admin.TabularInline):
    model = OfferLink
    extra = 0
    fields = ('source', 'link', 'title')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('user_ip', 'links', 'created')
    ordering = ('-created',)
    readonly_fields = ('user',)
    list_display_links = None

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('user',)
        }),
        ('RAW', {
            'fields': ('text',)
        }),
        # ('MEDIA', {
        #     'fields': ('picture', 'picture_thumbnail',)
        # }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )

    inlines = [
        OfferLinkInline
    ]

    def user_ip(self, obj):
        return obj.user.ip

    def links(self, obj):
        links = OfferLink.objects.filter(offer=obj)
        string = ''
        for idx, link in enumerate(links):
            if not link.title:
                link.title = link.link
            string += f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{link.link}'>{idx + 1}. {link.title}</a><br/>"
        return format_html(string)


admin.site.register(Offer, OfferAdmin)


class OfferLinkAdmin(admin.ModelAdmin):
    list_display = ('_link', 'title', 'source', 'user_ip', 'created')
    list_display_links = None
    ordering = ('-created',)
    list_filter = ('source',)
    search_fields = ('title',)

    def user_ip(self, obj):
        if obj.offer.user:
            return obj.offer.user.ip
        return None

    def _link(self, obj):
        if obj.source == 'youtube':
            # try to get id
            video_id = get_yt_video_id(obj.link)
            if video_id:
                return format_html(f"<iframe src='https://www.youtube.com/embed/{video_id}'></iframe>")

        if not obj.title:
            obj.title = obj.link

        return format_html(f"<a target='_blank' rel='noopener noreferrer' class='js-video-button' href='{obj.link}'>{obj.title}</a><br/>")



admin.site.register(OfferLink, OfferLinkAdmin)
