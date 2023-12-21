from django.urls import path
from . import views

from .views import (
    create_review,
    get_review_by_id,
    get_reviews_for_me,
    get_reviews,
    edit_review,
)

urlpatterns = [
    path('all/', get_reviews, name='Get All Reviews'),
    path('create/', create_review, name='Create Review'),
    path('me/', get_reviews_for_me, name='Get Reviews for Me'),
    path('<str:review_id>/', get_review_by_id, name='Get Review'),
    path('<str:review_id>/edit/', edit_review, name='Edit Review'),
]
