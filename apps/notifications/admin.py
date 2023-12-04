from django.contrib import admin

from apps.core.admin import prompt_admin

from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'read')
    list_filter = ('user', 'order', 'read')
    search_fields = ('user', 'order', 'text')

# Register your models here.

prompt_admin.register(Notification, NotificationAdmin)