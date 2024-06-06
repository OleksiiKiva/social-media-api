from django.conf import settings
from django.db import models

from core.upload_image_to import UploadImageTo


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to=UploadImageTo("profiles/"), blank=True, null=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Post(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(
        upload_to=UploadImageTo("posts/"), blank=True, null=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post by {self.author} at {self.created_at}"
