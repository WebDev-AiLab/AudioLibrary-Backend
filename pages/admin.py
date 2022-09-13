from django.contrib import admin
from .models import Page, PageMain, PageUser
from adminsortable2.admin import SortableAdminMixin

from django import forms


# from django.contrib.flatpages.models import FlatPage
# from tinymce.widgets import TinyMCE


# class FlatPageForm(forms.ModelForm):
#     content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
#
#     class Meta:
#         model = FlatPage
#         exclude = []


# Register your models here.

# class PageAdmin(SortableAdminMixin, admin.ModelAdmin):
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order', 'url_mask', 'type', 'created')
    list_editable = ('order',)
    ordering = ('section', 'order',)
    search_fields = ('title', 'slug', 'url_mask')
    readonly_fields = ('slug',)

    list_filter = ('type',)

    save_on_top = True

    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('title', 'url_mask', 'section', 'type')
        }),
        ('CONTENT', {
            'fields': ('content',)
        }),
        ('FRONTEND', {
            'fields': ('page',)
        }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )

    class Media:
        js = (
            '/media/js/admin-page-content.js',
        )
        css = {
            'screen': ('/media/css/ckeditor.css', '/media/css/custom.admin.css', '/media/css/custom.admin.pages.css')
        }


admin.site.register(Page, PageAdmin)


# class PageMainAdmin(PageAdmin):
#     def get_queryset(self, request):
#         qs = super(PageMainAdmin, self).get_queryset(request)
#         return qs.filter(section='Main')
#
#     fieldsets = (
#         ('GENERAL INFORMATION', {
#             'fields': ('title', 'url_mask', 'type')
#         }),
#         ('CONTENT', {
#             'fields': ('content',)
#         }),
#         ('FRONTEND', {
#             'fields': ('page',)
#         }),
#         ('SYSTEM', {
#             'fields': ('created',)
#         }),
#     )
#
#
# admin.site.register(PageMain, PageMainAdmin)
#
#
# class PageUserAdmin(PageAdmin):
#     def get_queryset(self, request):
#         qs = super(PageUserAdmin, self).get_queryset(request)
#         return qs.filter(section='User')
#
#     fieldsets = (
#         ('GENERAL INFORMATION', {
#             'fields': ('title', 'url_mask', 'type')
#         }),
#         ('CONTENT', {
#             'fields': ('content',)
#         }),
#         ('FRONTEND', {
#             'fields': ('page',)
#         }),
#         ('SYSTEM', {
#             'fields': ('created',)
#         }),
#     )
#
#
# admin.site.register(PageUser, PageUserAdmin)
