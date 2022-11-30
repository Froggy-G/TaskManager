from rest_framework import viewsets
from main.models import User, Task, Tag
from main.serializers import UserSerializer, TaskSerializer, TagSerializer
from django_filters import (
    FilterSet,
    CharFilter,
    ChoiceFilter,
    ModelMultipleChoiceFilter,
)
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated


class ActionBasedPermission(AllowAny):
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class UserFilter(FilterSet):
    username = CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = [
            "username",
        ]


class TaskFilter(FilterSet):
    status = ChoiceFilter(choices=Task.Status.choices)
    tags = ModelMultipleChoiceFilter(
        field_name="tags__title", queryset=Tag.objects.all()
    )
    author = CharFilter(field_name="user__username", lookup_expr="icontains")
    executor = CharFilter(field_name="user__username", lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ["status", "tags", "author", "executor"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['destroy', 'create', 'update', 'partial_update'],
        IsAuthenticated: ['list', 'retrieve'],
    }


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "executor")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['destroy'],
        IsAuthenticated: ['update', 'partial_update', 'list', 'create', 'retrieve'],
    }


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAdminUser: ['destroy'],
        IsAuthenticated: ['update', 'partial_update', 'list', 'create', 'retrieve'],
    }
