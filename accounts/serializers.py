from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:

            raise serializers.ValidationError(
                "Invalid username or password."
            )

        if not user.is_active:

            raise serializers.ValidationError(
                "User account is inactive."
            )

        attrs["user"] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_superuser",
        ]


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField()

    new_password = serializers.CharField(
        min_length=6
    )