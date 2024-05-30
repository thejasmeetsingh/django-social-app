import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email


class FriendRequest(models.Model):
    """
    Store friend request sent by a user to other user, 
    Also have a field to show the status of the friend request:
    - P: Pending
    - A: Accept
    - R: Reject
    """

    class StatusType(models.TextChoices):
        PENDING = "P"
        ACCEPT = "A"
        REJECT = "R"

    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    from_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="request_sent")
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="request_receive")
    status = models.CharField(
        max_length=2, choices=StatusType, default=StatusType.PENDING)

    class Meta:
        ordering = ("-created_at",)
