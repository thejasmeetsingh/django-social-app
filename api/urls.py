from django.urls import path

from api.views import auth, friend_request

urlpatterns = [
    path("login/", auth.Login.as_view(), name="login"),
    path("signup/", auth.Signup.as_view(), name="signup"),

    path("user/", friend_request.UserListView.as_view(), name="user-list"),
    path("friend-request/", friend_request.FriendRequestListView.as_view(),
         name="friend-request"),
    path("friend-request/<str:pk>/", friend_request.FriendRequestUpdateView.as_view(),
         name="update-friend-request")
]
