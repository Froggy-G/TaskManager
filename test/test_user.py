from base_test_class import TestViewSetBase
from factories import factory, UserFactory
from http import HTTPStatus


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
    users_attributes = factory.build_batch(dict, FACTORY_CLASS=UserFactory, size=5)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response
    
    def test_retrieve(self):
        user = self.create(self.user_attributes)
        response = self.retrieve(user["id"])
        expected_response = self.expected_details(user, self.user_attributes)
        assert response == expected_response
    
    def test_update(self):
        user = self.create(self.user_attributes)
        new_data = {
            "role": "admin",
        }
        updated_attributes = dict(self.user_attributes, **new_data)
        expected_response = self.expected_details(user, updated_attributes)
        response = self.update(new_data, user["id"])
        assert response == expected_response

    def test_delete(self):
        admin_test = self.retrieve(self.user.id)
        user = self.create(self.user_attributes)
        self.delete(user["id"])
        users = self.list()
        assert users == [admin_test, ]

    def test_list(self):
        admin_test = self.retrieve(self.user.id)
        users = self.create_list(self.users_attributes)
        users.insert(0, admin_test)
        response = self.list()
        assert response == users

    def test_filter(self):
        filter_name = "username"
        filter_value = "a"
        admin_test = self.retrieve(self.user.id)
        users = self.create_list(self.users_attributes)
        users.insert(0, admin_test)
        filtered_users: list = []
        for user in users:
            for char in user[filter_name]:
                if char == filter_value:
                    filtered_users.append(user)
                    break
        response = self.filter(filter=filter_name, filter_value=filter_value)
        assert response == filtered_users

    def test_unauntificated_request(self):
        response = self.unauntificated_request()
        assert response.status_code == HTTPStatus.FORBIDDEN
        