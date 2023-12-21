from django.urls import path
from . import views

from .views import (
    create_review
)

urlpatterns = [
    path('create/', create_review, name='Create Review'),
]
