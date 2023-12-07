import datetime

from django.db import models
from datetime import timedelta
import time
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

import uuid


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(blank=True, unique=True)
    profile_picture = models.ImageField(upload_to='pfps', default='user_def.jpg')
    is_printer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    account_number = models.DecimalField(decimal_places=0, max_digits=20, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)


class Printer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    description = models.TextField()
    is_open = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=225)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    offers_coloured = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class OneTimePassword(models.Model):
    otp = models.CharField(max_length=5, blank=True)
    email = models.EmailField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(auto_now=True)
    # I'm using the dummy field to track changes in the otp to know the expiry date
    dummy = models.CharField(max_length=5, blank=False)

    def __str__(self):
        return self.email
