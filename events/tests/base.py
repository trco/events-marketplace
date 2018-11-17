from django.contrib.auth.models import User
from django.test import TestCase
from events.models import Event


class CustomTestCase(TestCase):
    def create_user(self, username, password):
        return User.objects.create_user(
            username=username,
            password=password
        )

    def create_event(self, title, user):
        return Event.objects.create(
            title=title,
            user=user
        )
