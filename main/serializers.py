from rest_framework import serializers
from .models import User, Task, Tag
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.core.files.base import File
from task_manager import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class FileMaxSizeValidator:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self.max_size:
            raise ValidationError(f"Maximum size {self.max_size} exceeded.")


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(settings.UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )

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
            "avatar_picture",
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
