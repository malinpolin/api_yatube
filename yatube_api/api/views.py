from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from posts.models import Post, Group

from api.serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
)

from api.permissions import IsAuthor, IsAuthenticated


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
