from django.contrib import admin

from news.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'author', 'created')
    ordering = ('-created',)
    search_fields = ('title', 'slug')
    # readonly_fields = ('slug',)

    save_on_top = True

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('MEDIA', {
            'fields': ('picture', 'picture_thumbnail',)
        }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )

    # save current user
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user

        obj.save()

    class Media:
        css = {
            'screen': ('/media/css/ckeditor.css',)
        }


admin.site.register(Post, PostAdmin)
