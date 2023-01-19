from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task
from task_manager.services.mail import send_assign_notification
from base_test_class import TestViewSetBase

from factories import UserFactory, BaseTaskFactory


class TestSendEmail(TestViewSetBase):
    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        executor = UserFactory.create()
        task = BaseTaskFactory.create(executor=executor)

        send_assign_notification(task.id)
        fake_sender.assert_called_once_with(
            subject="You've assigned a new task.",
            message="",
            from_email=None,
            recipient_list=[executor.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task.id)},
            ),
        )