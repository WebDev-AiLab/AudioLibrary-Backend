from datetime import timedelta, datetime

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Guest, UserOnline, UserContactForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from .models import User, UserGroup, UserVerificationData
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


# extending admin view
class UserAdmin(BaseUserAdmin):
    model = User
    readonly_fields = (
    '_raw_password', 'last_seen', 'date_joined', 'last_login', 'city', 'region', 'country', 'timezone', 'utc_offset',
    'latitude', 'longitude', 'ip', 'ipv', 'phpbb_id')
    list_editable = ('banned_by_ip',)
    fieldsets = (
        (None, {"fields": ("username", "_raw_password")}),
        (_("PERSONAL INFO"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("PERMISSIONS"),
            {
                "fields": (
                    # "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            _("SERVICES"),
            {
                "fields": (
                    "phpbb_id",
                ),
            },
        ),
        (_("IMPORTANT DATES"), {"fields": ("last_login", "date_joined", "last_seen")}),
        ('STATUS', {'fields': ('is_verified',)}),
        ('LOCATION INFO', {'fields': ('ip', 'ipv', 'city', 'region', 'country', 'timezone', 'latitude', 'longitude')}),
        ('TECH INFO', {'fields': ('browser', 'operating_system')}),
    )

    # fieldsets = BaseUserAdmin.fieldsets + (
    #     # ('Personal Information', {'fields': ('bio',)}),
    #     ('Status', {'fields': ('is_guest', 'is_verified')}),
    #     ('Tech', {'fields': ('browser', 'operating_system')}),
    #     # add more if you need
    # )
    list_display = (
    'username', 'email', 'last_seen', 'date_joined', 'ip', 'country', 'region', 'city', 'operating_system', 'browser',
    'banned_by_ip', 'stats', 'last_login')
    ordering = ('-date_joined',)
    # list_display = BaseUserAdmin.list_display + ('is_guest',)
    list_filter = ('is_active', 'is_verified', 'country', 'region', 'banned_by_ip')
    save_on_top = True

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        return qs.filter(is_guest=False)

    def stats(self, obj):
        return format_html("<a href='/admin/interactions/stat/?user_id__exact={}'>Stats</a>/<a href='/admin/interactions/commentartists/?user_id__exact={}'>CA</a>/<a href='/admin/interactions/commenttracks/?user_id__exact={}'>CT</a>", obj.id, obj.id, obj.id)

    # def current_local_time(self, obj):
    #     if obj.timezone:
    #         now = datetime.now(obj.timezone)
    #         return now.strftime("%H:%M:%S")
    #     return None


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


# admin.site.register(UserGroup, GroupAdmin)


class GuestAdmin(BaseUserAdmin):
    model = Guest
    list_display = ('ip', 'browser', 'operating_system', 'country', 'region', 'city', 'last_seen', 'banned_by_ip')
    ordering = ('-last_seen',)
    list_filter = ('country', 'region', 'banned_by_ip')
    list_editable = ('banned_by_ip',)
    list_display_links = None

    def get_queryset(self, request):
        qs = super(GuestAdmin, self).get_queryset(request)
        return qs.filter(is_guest=True)


admin.site.register(Guest, GuestAdmin)


class UserOnlineAdmin(BaseUserAdmin):
    model = UserOnline
    list_display = (
    'get_username', 'ip', 'browser', 'operating_system', 'country', 'region', 'city', 'last_seen', 'banned_by_ip')
    ordering = ('-last_seen',)
    list_filter = ('country', 'region')
    list_editable = ('banned_by_ip',)

    # list_display_links = None

    def get_queryset(self, request):
        qs = super(UserOnlineAdmin, self).get_queryset(request)
        ten_minutes = timezone.now() - timedelta(minutes=1)
        return qs.filter(last_seen__gte=ten_minutes, is_guest=False)

    def get_username(self, obj):
        url = f"/admin/accounts/user/{obj.id}/change/"
        return format_html("<a href='{}'>{}</a>", url, obj.username)


admin.site.register(UserOnline, UserOnlineAdmin)


class UserContactFormAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'text', 'ip', 'created')
    readonly_fields = ('email', 'text', 'ip', 'created', 'user')
    fieldsets = (
        ('GENERAL INFORMATION', {
            'fields': ('user', 'email', 'ip')
        }),
        ('CONTENT', {
            'fields': ('text',)
        }),
        ('SYSTEM', {
            'fields': ('created',)
        }),
    )
    ordering = ('-created',)


admin.site.register(UserContactForm, UserContactFormAdmin)

# class UserVerificationDataAdmin(admin.ModelAdmin):
#     list_display = ['user', 'target', 'created']
#     search_fields = ('user__username', 'target')
#     list_filter = ('status',)
#
#     fieldsets = (
#         ('GENERAL INFORMATION', {
#             'fields': ('user', 'target', 'status')
#         }),
#         ('SYSTEM', {
#             'fields': ('created',)
#         }),
#     )
#
#
# admin.site.register(UserVerificationData, UserVerificationDataAdmin)

# class GuestAdmin(UserAdmin):
#     def queryset(self, request):
#         return super(GuestAdmin, self).queryset(request).filter(is_guest=True)
#
#
# admin.site.register(User, GuestAdmin)
