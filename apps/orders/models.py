from django.db import models

from apps.authentication.models import User, Printer

import uuid

# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    # document = models.FileField(upload_to='files_to_print', max_length=200, blank=True, null=True)
    no_of_copies = models.IntegerField()
    pages = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order_time = models.DateTimeField(auto_now_add=True)
    time_expected = models.TimeField()
    is_complete = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    coloured = models.BooleanField(default=False)
    charge = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f'from {self.user} to {self.printer}'

class OrderDocument(models.Model):
    order_id = models.UUIDField()
    document = models.FileField(upload_to='files_to_print', max_length=200, blank=True, null=True)
    
     