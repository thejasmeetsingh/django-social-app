from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import serializers, status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin

import strings
from api.models import CustomUser, FriendRequest
from api.serializers import UserSerializer, FriendRequestSerializer


class UserListView(GenericAPIView, ListModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    search_fields = ("first_name", "last_name", "=email")

    def get_queryset(self):
        # Exclude current user from the queryset
        return super().get_queryset().exclude(id=self.request.user.id)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)


class FriendRequestListView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = FriendRequest.objects.select_related("from_user", "to_user")
    serializer_class = FriendRequestSerializer

    def initial(self, request: Request, *args, **kwargs):
        # Add throttling if the request is a POST request
        # So that user cannot create more than 3 request in a minute
        if request.method == "POST":
            self.throttle_scope = "friend_requests"
        return super().initial(request, *args, **kwargs)

    def handle_exception(self, exc: Exception):
        if isinstance(exc, KeyError):
            exc = serializers.ValidationError(detail={
                "data": None,
                "message": f"{exc.args[0]} field is required"
            }, code=status.HTTP_400_BAD_REQUEST)

        return super().handle_exception(exc)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = self.create(request, *args, **kwargs)
        response.data = {
            "data": response.data,
            "message": strings.REQUEST_SUCCESS
        }

        return response
