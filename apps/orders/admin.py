from django.contrib import admin

from apps.core.admin import prompt_admin

from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'printer', 'order_time', 'time_expected', 'pay_on_collection', 'paid', 'is_complete')
    list_filter = ('user', 'printer', 'pay_on_collection', 'paid', 'is_complete')
    search_fields = ('user', 'printer', 'order_time')

# Register your models here.
prompt_admin.register(Order, OrderAdmin)