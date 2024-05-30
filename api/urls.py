from django.urls import path

from api.views import auth, friend_request

urlpatterns = [
    path("login/", auth.Login.as_view(), name="login"),
    path("signup/", auth.Signup.as_view(), name="signup"),
    path("user/", friend_request.UserListView.as_view(), name="user-list")
]
