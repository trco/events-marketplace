from django.test import TestCase
from events.models import Event


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
