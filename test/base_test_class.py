from rest_framework.test import APIClient, APITestCase
from main.models import User
from django.urls import reverse
from typing import Union, List
from http import HTTPStatus
from factories import factory, SuperUserFactory
from functools import partial


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()

    @staticmethod
    def create_api_user():
        user_attributes = factory.build(dict, FACTORY_CLASS=SuperUserFactory)
        return User.objects.create(**user_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @classmethod
    def list_url_filter(cls, filter: str = None, filter_value: str = None) -> str:
        url = reverse(f"{cls.basename}-list")
        return f"{url}?{filter}={filter_value}"

    def create(
        self, data: dict, args: List[Union[str, int]] = None, format: str = "json"
    ) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.post(self.list_url(args), data=data, format=format)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def retrieve(self, id: int = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.detail_url(id))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, data: dict, id: int = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.detail_url(id), data=data, format="json")
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, id: int = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.detail_url(id))
        assert response.status_code == HTTPStatus.NO_CONTENT
        return response

    def create_list(self, data: list[dict], format: str = "json") -> list[dict]:
        return list(map(partial(self.create, format=format), data))

    def list(self) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url())
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def filter(self, filter: str = None, filter_value: str = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url_filter(filter, filter_value))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def unauthenticated_request(self):
        self.client.logout()
        response = self.client.get(self.list_url())
        return response
