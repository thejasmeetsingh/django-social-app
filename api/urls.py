from django.urls import path

from api.views import auth

urlpatterns = [
    path("login/", auth.Login.as_view(), name="login"),
    path("signup/", auth.Signup.as_view(), name="signup")
]
