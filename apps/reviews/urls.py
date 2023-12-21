from django.urls import path
from . import views

from .views import (
    create_review,
    get_review_by_id,
)

urlpatterns = [
    path('create/', create_review, name='Create Review'),
    path('<str:review_id>/', get_review_by_id, name='Get Review'),
]
