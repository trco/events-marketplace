from django.test import TestCase
from events.forms import EventForm
from events.models import Event
from .base import CustomTestCase


class CreateEventFormTest(CustomTestCase):

    def setUp(self):
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        # login
        self.client.login(username='user_1', password='test1234')

    def test_invalid_title_length(self):
        form = EventForm(data={'title': 'a'*129})
        self.assertFalse(form.is_valid())

    def test_user_is_set_as_event_user_on_save(self):
        form = EventForm(data={'title': 'Test event #1'})
        form.save(user=self.user_1)
        event = Event.objects.first()
        self.assertEqual(self.user_1, event.user)

    def test_form_handles_saving_to_database(self):
        form = EventForm(data={'title': 'Test event #1'})
        new_event = form.save(user=self.user_1)
        event = Event.objects.first()
        self.assertEqual(new_event, event)
