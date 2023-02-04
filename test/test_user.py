from base_test_class import TestViewSetBase
from factories import factory, UserFactory, LargeAvatarUserFactory
from http import HTTPStatus


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    
    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    def test_create(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes, format="multipart")
        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

    def test_retrieve(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes, format="multipart")
        response = self.retrieve(user["id"])
        expected_response = self.expected_details(user, user_attributes)
        assert response == expected_response

    def test_update(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes, format="multipart")
        new_data = {
            "role": "admin",
        }
        updated_attributes = dict(user, **new_data)
        expected_response = self.expected_details(user, updated_attributes)
        expected_response["avatar_picture"] = updated_attributes["avatar_picture"]
        response = self.update(new_data, user["id"])
        assert response == expected_response

    def test_delete(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        admin_test = self.retrieve(self.user.id)
        user = self.create(user_attributes, format="multipart")
        self.delete(user["id"])
        users = self.list()
        assert users == [
            admin_test,
        ]

    def test_list(self):
        admin_test = self.retrieve(self.user.id)
        users_attributes = factory.build_batch(dict, FACTORY_CLASS=UserFactory, size=5)
        users = self.create_list(users_attributes, format="multipart")
        users.insert(0, admin_test)
        response = self.list()
        assert response == users

    def test_filter(self):
        users_attributes = factory.build_batch(dict, FACTORY_CLASS=UserFactory, size=5)
        filter_name = "username"
        filter_value = "a"
        admin_test = self.retrieve(self.user.id)
        users = self.create_list(users_attributes, format="multipart")
        users.insert(0, admin_test)
        expected_users: list = []
        for user in users:
            for char in user[filter_name]:
                if char == filter_value:
                    expected_users.append(user)
                    break
        response = self.filter(filter=filter_name, filter_value=filter_value)
        assert response == expected_users

    def test_unauthenticated_request(self):
        response = self.unauthenticated_request()
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_large_avatar(self) -> None:
        self.client.force_authenticate(self.user)
        user_attributes = factory.build(dict, FACTORY_CLASS=LargeAvatarUserFactory)
        response = self.client.post(self.list_url(), data=user_attributes, format="multipart")
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture":["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        self.client.force_authenticate(self.user)
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.client.post(self.list_url(), data=user_attributes, format="multipart")
        print(response)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }