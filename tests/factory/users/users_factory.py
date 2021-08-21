import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    id = factory.Faker("pyint", min_value=0, max_value=10000)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "user-%d" % n)
    is_staff = False
    is_superuser = False
    password = "secret"

    @factory.lazy_attribute
    def email(self):
        return "%s@test.com" % self.username

    class Meta:
        model = User

    class Params:
        flag_is_superuser = factory.Trait(
            is_superuser=True,
            is_staff=True,
            username=factory.Sequence(lambda n: "admin-%d" % n),
        )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", None)
        obj = super(UserFactory, cls)._create(model_class, *args, **kwargs)
        obj.set_password(password)
        obj.save()
        return obj
