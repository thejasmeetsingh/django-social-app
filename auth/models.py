import uuid
from typing import Collection

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email

    def validate_unique(self, exclude: Collection[str] | None = ...) -> None:
        """
        Make email lowercase before validating the unique constraint
        """

        if not self.email.islower():
            self.email = self.email.lower()
        return super().validate_unique(exclude=["id"])
