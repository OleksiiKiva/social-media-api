from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.models import Profile
from core.serializers import ProfileSerializer


class ProfileViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")
        username = self.request.query_params.get("username")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if username:
            queryset = queryset.filter(username__icontains=username)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset
