from django.contrib import admin

from apps.core.admin import prompt_admin

from .models import Transaction, Wallet

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'printer', 'amount')
    list_filter = ('user', 'printer')
    search_fields = ('user', 'printer')
    
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    list_filter = ('user',)
    search_fields = ('user',)

# Register your models here.
prompt_admin.register(Transaction, TransactionAdmin)
prompt_admin.register(Wallet, WalletAdmin)