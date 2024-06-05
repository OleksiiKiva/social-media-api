import pathlib
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def profile_image_path(instance: "Profile", filename: str) -> pathlib.Path:
    filename = (
        f"{slugify(instance.username)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/profiles/") / pathlib.Path(filename)


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
        blank=True, null=True, upload_to=profile_image_path
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
