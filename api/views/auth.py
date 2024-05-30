from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

import strings
from api.serializers import SignupSerializer
from api.utils import get_auth_token


class BaseAuthView(APIView):
    permission_classes = (AllowAny,)

    def handle_exception(self, exc):
        if isinstance(exc, KeyError):
            exc = serializers.ValidationError(detail={
                "message": f"{exc.args[0]} field is required"
            })

        return super().handle_exception(exc)


class Login(BaseAuthView):
    def post(self, request: Request) -> Response:
        user = authenticate(
            request,
            username=request.data["email"].lower(),
            password=request.data["password"]
        )

        if not user:
            return Response({"data": None, "message": strings.INVALID_LOGIN}, status=status.HTTP_403_FORBIDDEN)

        # Update last login timestamp
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        tokens = get_auth_token(user)

        return Response({"data": tokens, "message": strings.LOGIN_SUCCESS}, status=status.HTTP_200_OK)


class Signup(BaseAuthView):
    def post(self, request: Request) -> Response:
        serializer = SignupSerializer(data=request.data, context={
                                      "request": request, "view": self})
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        tokens = get_auth_token(user)

        return Response({"data": tokens, "message": strings.SIGNUP_SUCCESS}, status=status.HTTP_201_CREATED)
