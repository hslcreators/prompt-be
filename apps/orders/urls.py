from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_order, name="Create Order"),
    path("printer/", views.get_orders_by_printer, name="Get ALl Orders By Printer"),
    path("user/", views.get_orders_by_user, name="Get ALl Orders By Users"),
    path("<order_id>/", views.get_order_by_id, name="Get Order By Order Id"),
    path("schedule/<order_id>", views.get_order_schedule, name="Get Order Schedule"),
    path("update/<order_id>/", views.update_complete_status, name="Update Order Status")
]
