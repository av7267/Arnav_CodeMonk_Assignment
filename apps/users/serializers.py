from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer used for returning user information
    in API responses.
    """

    class Meta:
        model = User

        fields = (
            "id",
            "name",
            "email",
            "date_of_birth",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles validation and creation
    of new user accounts.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User

        fields = (
            "id",
            "name",
            "email",
            "date_of_birth",
            "password",
        )

    def create(self, validated_data):
        """
        Create a new user using Django's
        built-in create_user method so the
        password is securely hashed.
        """

        new_user = User.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            date_of_birth=validated_data["date_of_birth"],
            password=validated_data["password"],
        )

        return new_user