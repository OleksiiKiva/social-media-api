from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import ProfileViewSet, PostViewSet

app_name = "core"


router = DefaultRouter()
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("posts", PostViewSet, basename="posts")


urlpatterns = [path("", include(router.urls))]
