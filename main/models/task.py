from django.db import models
from .user import User
from .tag import Tag


class Task(models.Model):
    class Status(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    class Priority(models.TextChoices):
        VERY_HIGH = "very_high"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    date_of_creation = models.DateField()
    date_of_change = models.DateField()
    date_of_completion = models.DateField()
    status = models.CharField(
        max_length=255, default=Status.NEW_TASK, choices=Status.choices
    )
    priority = models.CharField(
        max_length=255, default=Priority.MEDIUM, choices=Priority.choices
    )
    author = models.ForeignKey(
        User, related_name="user_author", on_delete=models.SET_NULL, null=True
    )
    executor = models.ForeignKey(
        User, related_name="user_executor", on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag)
