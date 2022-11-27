import factory
from faker import Faker


faker = Faker()

class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.user'

    username = factory.LazyAttribute(lambda _: faker.user_name())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    role = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "developer",
                "manager",
                "admin",
            ]
        )
    )
    is_staff = True

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.user'

    username = factory.LazyAttribute(lambda _: faker.user_name())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    role = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "developer",
                "manager",
                "admin",
            ]
        )
    )

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.tag'

    title = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=50))

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'main.task'

    title = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=50))
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=500))
    date_of_change = factory.LazyAttribute(lambda _: faker.past_date().strftime("%Y-%m-%d"))
    date_of_completion = factory.LazyAttribute(lambda _: faker.future_date().strftime("%Y-%m-%d"))
    status = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "new_task",
                "in_development",
                "in_qa",
                "in_code_review",
                "ready_for_release",
                "released",
                "archived",
            ]
        )
    )
    priority = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "very_high",
                "high",
                "medium",
                "low",
            ]
        )
    )
    executor = None
    tags = []