from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_order, name="Create Order"),
    path("<order_id>", views.get_order_by_id, name="Get Order By Order Id")
]
