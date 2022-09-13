from django.contrib import admin
from .models import Subscriber


# Register your models here.
class SubscriberAdmin(admin.ModelAdmin):
    model = Subscriber
    list_display = ('email', 'created')
    ordering = ('-created',)


# admin.site.register(Subscriber, SubscriberAdmin)
