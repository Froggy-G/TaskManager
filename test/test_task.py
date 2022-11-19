from base_test_class import TestViewSetBase
from factories import factory, TaskFactory
from http import HTTPStatus


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    task_attributes = factory.build(dict, FACTORY_CLASS=TaskFactory)
    tasks_attributes = factory.build_batch(dict, FACTORY_CLASS=TaskFactory, size=5)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, self.task_attributes)
        assert task == expected_response

    def test_retrieve(self):
        task = self.create(self.task_attributes)
        response = self.retrieve(task["id"])
        expected_response = self.expected_details(task, self.task_attributes)
        assert response == expected_response

    def test_update(self):
        task = self.create(self.task_attributes)
        new_data = {
            "title": "Create tests",
            "description": "I'm so tired of making these test's"
        }
        updated_attributes = dict(self.task_attributes, **new_data)
        expected_response = self.expected_details(task, updated_attributes)
        response = self.update(new_data, task["id"])
        assert response == expected_response
    
    def test_delete(self):
        task = self.create(self.task_attributes)
        response = self.delete(task["id"])
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_list(self):
        tasks = self.create_list(self.tasks_attributes)
        response = self.list()
        assert response == tasks
    
    def test_filter(self):
        filter_name = "status"
        filter_value = "new_task"
        tasks = self.create_list(self.tasks_attributes)
        filtered_tasks: list = []
        for task in tasks:
            for field in task:
                if field == filter_name and filter_value == task[filter_name]:
                    filtered_tasks.append(task)
        response = self.filter(filter=filter_name, filter_value=filter_value)
        assert response == filtered_tasks
        