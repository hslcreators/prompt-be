from django.urls import path
from . import views

urlpatterns = [
    path("user/signup/", views.create_user, name="Sign Up"),
    path("user/login/", views.login, name="Log in"),
    path("verify-otp/", views.verify_token, name="Verify OTP"),
    path("generate-otp/", views.generate_otp, name="Generate OTP"),
    path("printer/create/", views.create_printer, name="Create Printer"),
    path("vendor/update-rates/", views.update_rates, name="Update Printing Rates"),
    path("user/reset-password/", views.reset_password, name="Reset Password"),
    path("user/send-reset-password-link/", views.send_reset_password_link, name="Send Reset Password Link"),
    path("user/logout", views.logout, name="Log Out"),
    path("user/change-password", views.change_password, name="Change Password"),
    path("vendor/<printer_id>", views.find_printer_by_id, name="Find Printer By Id"),
    path("vendors", views.find_printers_by_location, name="Find Printer By Location"),
    path("vendor/all/", views.find_all_printers, name="Find All Printers"),
    path("vendor/locations/", views.find_all_locations, name="Find all Printer Locations")
]
