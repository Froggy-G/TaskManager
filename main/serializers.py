from rest_framework import serializers
from .models import User, Task, Tag
from drf_writable_nested.serializers import WritableNestedModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "title",
        ]


class TaskSerializer(WritableNestedModelSerializer):
    executor = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "date_of_change",
            "date_of_completion",
            "status",
            "priority",
            "executor",
            "tags",
        ]
