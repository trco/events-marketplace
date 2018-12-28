"""
from events.forms import EventForm
from events.models import Event
from .base import CustomTestCase


class CreateEventFormTest(CustomTestCase):

    def setUp(self):
        # create user
        self.user = self.create_user('user', 'test1234')
        # login
        self.client.login(username='user', password='test1234')

    def test_invalid_title_length(self):
        form = EventForm(data={'title': 'a'*129})
        self.assertFalse(form.is_valid())

    def test_user_is_set_as_event_user_on_save(self):
        form = EventForm(data={'title': 'Test event #1'})
        form.save(user=self.user)
        event = Event.objects.first()
        self.assertEqual(self.user, event.user)

    def test_form_handles_saving_to_database(self):
        form = EventForm(data={'title': 'Test event #1'})
        new_event = form.save(user=self.user)
        event = Event.objects.first()
        self.assertEqual(new_event, event)
"""
