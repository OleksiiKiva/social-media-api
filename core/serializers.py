from rest_framework import serializers

from core.models import Profile, Post


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


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source="author.username", read_only=True
    )
    author_full_name = serializers.CharField(
        source="author.full_name", read_only=True
    )
    author_image = serializers.ImageField(
        source="author.profile_image", read_only=True
    )
    post_image = serializers.ImageField(required=False, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author_username",
            "author_full_name",
            "author_image",
            "content",
            "post_image",
            "created_at",
        )


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "post_image")
