from django.contrib import admin
from .models import UploadTrack, UploadArtists


@admin.register(UploadArtists)
class UploadArtistsAdmin(admin.ModelAdmin):
    change_list_template = 'admin/upload_artists_change_list.html'


@admin.register(UploadTrack)
class UploadArtistsAdmin(admin.ModelAdmin):
    change_list_template = 'admin/upload_tracks_change_list.html'
