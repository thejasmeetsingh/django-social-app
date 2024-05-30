from rest_framework import serializers
from rest_framework.validators import UniqueValidator

import strings
from api.models import CustomUser


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        UniqueValidator(
            queryset=CustomUser.objects.all(),
            message=strings.EMAIL_EXISTS,
            lookup="iexact"
        )
    ])

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")
