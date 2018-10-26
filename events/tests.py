from django.test import TestCase
from .models import Event


class HomePageTest(TestCase):
    def test_index_visit(self):
        response = self.client.get('/')
        self.assertContains(response, 'Events Marketplace')
        self.assertContains(response, 'Add Event')

    def test_go_to_create_event(self):
        response = self.client.get('/events/add')
        self.assertContains(response, 'Add Event')

    def test_display_events_at_index(self):
        event_one = Event.objects.create(title='Test event #1')
        event_two = Event.objects.create(title='Test event #2')

        response = self.client.get(f'/')

        self.assertContains(response, 'Test event #1')
        self.assertContains(response, 'Test event #2')


class CreateEventTest(TestCase):
    def test_create_event_post(self):
        response = self.client.post(
            '/events/add',
            data={'title_text': 'Test title #1'}
        )
        self.assertEqual(Event.objects.count(), 1)
        new_event = Event.objects.first()
        self.assertEqual(new_event.title, 'Test title #1')

    def test_redirect_after_post(self):
        response = self.client.post(
            '/events/add',
            data={'title_text': 'Test title #1'}
        )
        new_event = Event.objects.first()
        self.assertRedirects(response, f'/events/add')

    def test_display_events(self):
        event_one = Event.objects.create(title='Test event #1')
        event_two = Event.objects.create(title='Test event #2')

        response = self.client.get(f'/events/add')

        self.assertContains(response, 'Test event #1')
        self.assertContains(response, 'Test event #2')


class EventModelTest(TestCase):
    def test_create_read_event(self):
        # create events
        event_one = Event()
        event_one.title = 'Test event #1'
        event_one.save()

        event_two = Event()
        event_two.title = 'Test event #2'
        event_two.save()

        # read events
        events = Event.objects.all()
        self.assertEqual(events.count(), 2)

        saved_event_one = events[0]
        saved_event_two = events[1]

        self.assertIn('Test event #1', saved_event_one.title)
        self.assertIn('Test event #2', saved_event_two.title)
