from django.contrib.auth.models import User
from django.test import TestCase
from events.models import Event
from tickets.models import Ticket


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

    def create_ticket(self, name, event):
        return Ticket.objects.create(
            name=name,
            event=event
        )
