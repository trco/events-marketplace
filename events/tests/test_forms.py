from events.forms import EventForm, SearchEventsForm
from events.models import Event
from .base import CustomTestCase


class SearchEventsFormTest(CustomTestCase):

    def test_displays_search_events_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], SearchEventsForm)

    def test_get_success(self):
        response = self.client.get(f'/events/search/?q=test')
        self.assertEqual(response.status_code, 200)


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
