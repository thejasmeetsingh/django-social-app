from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin

from api.models import CustomUser, FriendRequest
from api.serializers import UserSerializer, FriendRequestSerializer


class UserListView(GenericAPIView, ListModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    search_fields = ("first_name", "last_name", "=email")

    def get_queryset(self):
        # Exclude current user from the queryset
        return super().get_queryset().exclude(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
