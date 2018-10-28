from django.contrib.auth.models import User
from django.test import TestCase
from .models import Event


class LoginLogoutTest(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create_user(
            username='user',
            password='test1234'
        )

    def test_login_logout(self):
        # login
        response = self.client.login(
            username='user',
            password='test1234'
        )
        response = self.client.get('/')
        # check that the user is logged in
        self.assertEqual(str(response.context['user']), 'user')

        # logout
        response = self.client.logout()
        response = self.client.get('/')
        # check that the user is logged out
        self.assertEqual(str(response.context['user']), 'AnonymousUser')


class IndexViewTest(TestCase):
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

        response = self.client.get('/')

        self.assertContains(response, 'Test event #1')
        self.assertContains(response, 'Test event #2')


class LoginRedirectionViewTest(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create_user(
            username='user',
            password='test1234'
        )

    def test_login_redirection(self):
        # login
        self.client.login(username='user', password='test1234')

        response = self.client.get('/login/redirection/')
        username = self.user.username
        self.assertRedirects(response, f'/profile/{ username }')


class UserProfileTest(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create_user(
            username='user',
            password='test1234'
        )
        self.new_event = Event.objects.create(title='Test event #1')

    def test_display_user_events(self):
        username = self.user.username
        response = self.client.get(f'/profile/{ username }')
        self.assertContains(response, 'Test event #1')


class CreateEventViewTest(TestCase):
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
        self.assertRedirects(response, '/events/add')

    def test_display_events(self):
        event_one = Event.objects.create(title='Test event #1')
        event_two = Event.objects.create(title='Test event #2')

        response = self.client.get('/events/add')

        self.assertContains(response, 'Test event #1')
        self.assertContains(response, 'Test event #2')
        # check Edit button
        self.assertContains(response, 'Edit')


class UpdateEventViewTest(TestCase):
    def test_update_event_post(self):
        event = Event.objects.create(title='Test event #1')
        response = self.client.post(
            f'/events/edit/{ event.id }',
            data={'title_text': 'Test title #2'}
        )

        self.assertEqual(Event.objects.count(), 1)
        updated_event = Event.objects.first()
        self.assertEqual(updated_event.title, 'Test title #2')

    def test_redirect_after_post(self):
        event = Event.objects.create(title='Test event #1')
        response = self.client.post(
            f'/events/edit/{ event.id }',
            data={'title_text': 'Test title #2'}
        )
        self.assertRedirects(response, '/events/add')


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
