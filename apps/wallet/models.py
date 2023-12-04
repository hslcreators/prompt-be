from django.db import models

from apps.authentication.models import User, Printer

ttypes = (
    ('CREDIT', 'Credit'),
    ('DEBIT', 'Debit'),
)

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    transaction_type = models.CharField(max_length=150, choices=ttypes)
  
def __str__(self):
    return f'{self.user.username} paid {self.amount} to {self.printer}'

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transactions = models.ManyToManyField(Transaction, related_name='is_for', blank=True)
    
    def __str__(self):
        return f'{self.user.username}\'s wallet' 