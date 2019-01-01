from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from events.models import Event


class EventModelTest(TestCase):

    def test_create_event(self):
        event = Event.objects.create(
            title='Event 1',
            start_date='2019-01-01',
            end_date='2019-01-07',
            email='test@test.com',
            website='http://test.com',
            address='9 Tabard Street, London, UK',
            active=True,
            deleted=False
        )

        events = Event.objects.all()
        self.assertEqual(events.count(), 1)

        self.assertEqual(event.title, 'Event 1')
        self.assertEqual(event.start_date, '2019-01-01')
        self.assertEqual(event.end_date, '2019-01-07')
        self.assertEqual(event.email, 'test@test.com')
        self.assertEqual(event.website, 'http://test.com')
        self.assertEqual(event.address, '9 Tabard Street, London, UK')
        self.assertEqual(event.locality, 'London')
        self.assertEqual(event.country, 'United Kingdom')
        self.assertEqual(event.latitude, 51.5008598)
        self.assertEqual(event.longitude, -0.0916454)
        self.assertEqual(event.active, True)
        self.assertEqual(event.deleted, False)
        today = datetime.today().strftime('%Y-%m-%d')
        self.assertEqual(event.created_at.strftime('%Y-%m-%d'), today)

    def test_event_is_related_to_user(self):
        user = User.objects.create_user(username='user', password='test1234')
        event = Event.objects.create(
            title='Event 1',
            user=user
        )
        self.assertIn(event, user.event_set.all())

    def test_string_representation(self):
        event = Event.objects.create(
            title='Event 1'
        )
        self.assertEqual(str(event), event.title)

    def test_cannot_save_event_without_title(self):
        event = Event.objects.create(title='')
        with self.assertRaises(ValidationError):
            event.save()
            event.full_clean()
