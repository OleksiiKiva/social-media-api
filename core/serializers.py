from rest_framework import serializers

from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model with update method for profile image"""

    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "profile_image",
            "user_email",
            "username",
            "first_name",
            "last_name",
            "bio",
        )

    def update(self, instance, validated_data):
        """If image is not included in request, don't update the image field"""

        if (
            "profile_image" not in validated_data
            or not validated_data["profile_image"]
        ):
            validated_data["profile_image"] = instance.profile_image
        return super().update(instance, validated_data)
