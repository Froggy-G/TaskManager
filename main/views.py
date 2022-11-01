from rest_framework import viewsets
from main.models import User, Task, Tag
from main.serializers import UserSerializer, TaskSerializer, TagSerializer
from django_filters import FilterSet, CharFilter, ChoiceFilter


class UserFilter(FilterSet):
    username = CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = [
            "username",
        ]


class TaskFilter(FilterSet):
    status = ChoiceFilter(choices=Task.Status.choices, default="NEW_TASK")
    tags = CharFilter(field_name="tag__title", lookup_expr="iexact")
    author = CharFilter(field_name="user__username", lookup_expr="icontains")
    executor = CharFilter(field_name="user__username", lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ["status", "tags", "author", "executor"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "executor")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
