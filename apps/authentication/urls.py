from django.urls import path
from . import views

urlpatterns = [
    path("sign-up/", views.create_user, name="Sign Up"),
    path("login/", views.login, name="Log in"),
    path("verify-otp/", views.verify_token, name="Verify Token")
]
