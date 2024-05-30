import uuid

from rest_framework_simplejwt.tokens import RefreshToken


def get_auth_token(user):
    """
    Retrieve auth tokens for a user
    """

    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Check if the given string contains a valid uuid or not
    """

    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False
