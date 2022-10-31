from rest_framework import viewsets
from main.models import User, Task, Tag
from main.serializers import UserSerializer, TaskSerializer, TagSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "executor")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
