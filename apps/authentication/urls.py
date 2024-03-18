from django.urls import path
from . import views

urlpatterns = [
    path("users/signup/", views.create_user, name="Sign Up"),
    path("users/login/", views.login, name="Log in"),
    path("verify-otp/", views.verify_token, name="Verify OTP"),
    path("generate-otp/", views.generate_otp, name="Generate OTP"),
    path("vendors/", views.create_printer, name="Create Printer"),
    path("vendors/update-rates/", views.update_rates, name="Update Printing Rates"),
    path("users/reset-password/", views.reset_password, name="Reset Password"),
    path("users/send-reset-password-link/", views.send_reset_password_link, name="Send Reset Password Link"),
    path("users/logout", views.logout, name="Log Out"),
    path("users/change-password", views.change_password, name="Change Password"),
    path("vendors/<printer_id>", views.find_printer_by_id, name="Find Printer By Id"),
    path("vendors", views.find_printers_by_location, name="Find Printer By Location"),
    path("vendors/all/", views.find_all_printers, name="Find All Printers"),
    path("vendors/locations/", views.find_all_locations, name="Find all Printer Locations")
]
