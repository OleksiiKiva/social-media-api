from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import ProfileViewSet


app_name = "core"


router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profiles")


urlpatterns = [path("", include(router.urls))]
