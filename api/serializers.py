from rest_framework import serializers
from rest_framework import status
from rest_framework.validators import UniqueValidator

import strings
from api.models import CustomUser, FriendRequest


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name")


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("id", "status", "created_at", "modified_at")

    def to_representation(self, instance: FriendRequest):
        data = super().to_representation(instance)

        # Send the details of other user, To whom the request is sent to or received from
        curr_user = self.context["request"].user
        other_user = instance.other_user if curr_user.id == instance.from_user_id else instance.from_user
        data.update({"user": UserSerializer(other_user, context=self.context)})

        return data

    def create(self, validated_data: dict):
        curr_user = self.context["request"].user

        # Check if user sent his/her own ID in the request
        if str(curr_user.id) == validated_data["user_id"]:
            raise serializers.ValidationError(
                detail={"user_id": strings.USER_ID_ERROR},
                code=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the record of other user
        other_user = CustomUser.objects.filter(
            id=validated_data["user_id"]).first()

        # Check if user exists in the system or not
        if not other_user:
            raise serializers.ValidationError(
                detail={"user_id": strings.USER_NOT_EXISTS},
                code=status.HTTP_400_BAD_REQUEST
            )

        validated_data.update({
            "from_user": curr_user,
            "to_user": other_user
        })

        return super().create(validated_data)
