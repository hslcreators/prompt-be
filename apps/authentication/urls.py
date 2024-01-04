from django.urls import path
from . import views

urlpatterns = [
    path("user/sign-up/", views.create_user, name="Sign Up"),
    path("user/login/", views.login, name="Log in"),
    path("verify-otp/", views.verify_token, name="Verify OTP"),
    path("generate-otp/", views.generate_otp, name="Generate OTP"),
    path("vendor/create-printer/", views.create_printer, name="Create Printer"),
    path("vendor/update-rates/", views.update_rates, name="Update Printing Rates"),
    path("user/reset-password/", views.reset_password, name="Reset Password"),
    path("user/send-reset-password-link/", views.send_reset_password_link, name="Send Reset Password Link"),
    path("user/logout", views.logout, name="Log Out"),
    path("user/change-password", views.change_password, name="Change Password")
]
