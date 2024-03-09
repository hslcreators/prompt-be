from django.contrib import admin

from apps.core.admin import prompt_admin

from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'printer', 'rating', 'created_at')
    list_filter = ('user', 'printer', 'rating')
    search_fields = ('user', 'printer', 'created_at', 'comment')

# Register your models here.
prompt_admin.register(Review, ReviewAdmin)