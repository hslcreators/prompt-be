from django.urls import path
from . import views

urlpatterns = [
    path("", views.create_order, name="Create Order"),
    path("printer/", views.get_orders_by_printer, name="Get ALl Orders By Printer"),
    path("user/", views.get_orders_by_user, name="Get ALl Orders By Users"),
    path("<order_id>", views.get_order_by_id, name="Get Order By Order Id"),
    path("schedule/<order_id>", views.get_order_schedule, name="Get Order Schedule"),
    path("active/", views.get_active_orders, name="Get Active Orders"),
    path("<order_id>/update", views.update_complete_status, name="Update Order Status"),
    path("document/<order_document_id>", views.get_order_document_by_id, name="Get Order Document By Id"),
    path("cron/", views.cron_job),
    path("delete/<key>", views.delete_all_orders, name="Delete All Orders At End Of The Day")
]
