from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import serializers, status
from rest_framework.exceptions import Throttled
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin

import strings
from api.permissions import CanUpdateRequest
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


class FriendRequestBaseView(GenericAPIView):
    queryset = FriendRequest.objects.select_related("from_user", "to_user")
    serializer_class = FriendRequestSerializer

    def handle_exception(self, exc: Exception):
        if isinstance(exc, KeyError):
            exc = serializers.ValidationError(detail={
                "message": f"{exc.args[0]} field is required"
            })

        # Send customize message for throttle exceptions
        if isinstance(exc, Throttled):
            exc = serializers.ValidationError(detail={
                "message": strings.REQUEST_LIMIT_ERROR
            })
            exc.status_code = status.HTTP_429_TOO_MANY_REQUESTS

        return super().handle_exception(exc)


class FriendRequestListView(FriendRequestBaseView, ListModelMixin, CreateModelMixin):
    queryset = FriendRequest.objects.select_related("from_user", "to_user")
    serializer_class = FriendRequestSerializer
    filterset_fields = ("status",)

    def initial(self, request: Request, *args, **kwargs):
        # Add throttling if the request is a POST request
        # So that user cannot create more than 3 request in a minute
        if request.method == "POST":
            self.throttle_scope = "friend_requests"
        return super().initial(request, *args, **kwargs)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = self.create(request, *args, **kwargs)
        response.data = {
            "data": response.data,
            "message": strings.REQUEST_SUCCESS
        }

        return response


class FriendRequestUpdateView(FriendRequestBaseView, UpdateModelMixin):
    permission_classes = (CanUpdateRequest,)

    def patch(self, request: Request, *args, **kwargs):
        response = self.partial_update(request, args, kwargs)
        response.data = {
            "data": response.data,
            "message": strings.REQUEST_UPDATE_SUCCESS
        }

        return response
