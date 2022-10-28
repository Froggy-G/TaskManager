from rest_framework import serializers
from models import User, Task, Tag


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
            "date_of_birth",
            "phone",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "title",
        ]


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer()

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "date_of_change",
            "date_of_completion",
            "status",
            "priority",
            "executor",
            "tags",
        ]
