from django.contrib import admin

from django.contrib.admin import AdminSite

class PromptAdminSite(AdminSite):
    site_title = 'Prompt Admin'
    site_header = 'Welcome to Prompt Admin!'
    index_title = 'Prompt Admin Home'

# Register your models here.
prompt_admin = PromptAdminSite(name='prompt_admin')
