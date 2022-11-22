from base_test_class import TestViewSetBase
from factories import factory, TagFactory
from http import HTTPStatus


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)
    tags_attributes = factory.build_batch(dict, FACTORY_CLASS=TagFactory, size=5)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_retrieve(self):
        tag = self.create(self.tag_attributes)
        response = self.retrieve(tag["id"])
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert response == expected_response

    def test_update(self):
        tag = self.create(self.tag_attributes)
        new_data = {
            "title": "Faster",
        }
        updated_attributes = dict(self.tag_attributes, **new_data)
        expected_response = self.expected_details(tag, updated_attributes)
        response = self.update(new_data, tag["id"])
        assert response == expected_response

    def test_delete(self):
        tag = self.create(self.tag_attributes)
        self.delete(tag["id"])
        tags = self.list()
        assert tags == []

    def test_list(self):
        tags = self.create_list(self.tags_attributes)
        response = self.list()
        assert response == tags
    
    def test_unauntificated_request(self):
        response = self.unauntificated_request()
        assert response.status_code == HTTPStatus.FORBIDDEN
        