from django.db import models

from apps.authentication.models import User, Printer

from apps.orders.models import Order

import uuid

# Create your models here.
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'notification for {self.user.username}'