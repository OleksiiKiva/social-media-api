from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models import Profile, Post
from core.permissions import IsAuthorOrReadOnly
from core.serializers import (
    ProfileSerializer,
    PostSerializer,
    PostImageSerializer,
)


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


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action == "upload_image":
            return PostImageSerializer

        return PostSerializer

    def get_queryset(self):
        queryset = Post.objects.select_related("author")
        content = self.request.query_params.get("content")
        author_username = self.request.query_params.get("author_username")

        if author_username is not None:
            queryset = queryset.filter(
                author__username__icontains=author_username
            )

        if content is not None:
            queryset = queryset.filter(content__icontains=content)

        return queryset

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Endpoint to upload an image to a post"""

        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"SUCCESS": "Image uploaded"},
            status=status.HTTP_204_NO_CONTENT,
        )
