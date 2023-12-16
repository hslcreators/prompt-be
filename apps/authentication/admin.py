from django.contrib import admin

from django.contrib.admin import AdminSite

from django.contrib.auth.admin import UserAdmin

from .models import User, OneTimePassword, Printer

from apps.core.admin import prompt_admin

# Register your models here.

prompt_admin.register(User, UserAdmin)

prompt_admin.register(Printer)

prompt_admin.register(OneTimePassword)
