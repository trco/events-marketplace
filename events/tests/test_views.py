from django.contrib.auth.models import User
from events.forms import EventForm
from events.models import Event
from .base import CustomTestCase


class IndexViewTest(CustomTestCase):

    def test_index_visit(self):
        response = self.client.get('/')
        self.assertContains(response, 'Events Marketplace')
        self.assertContains(response, 'Add Event')

    def test_go_to_create_event(self):
        User.objects.create_user(
            username='user',
            password='test1234'
        )
        # login
        self.client.login(username='user', password='test1234')
        response = self.client.get('/events/add')
        self.assertContains(response, 'Add Event')

    def test_display_events_at_index(self):
        event_one = Event.objects.create(title='Test event #1')
        event_two = Event.objects.create(title='Test event #2')

        response = self.client.get('/')

        self.assertContains(response, 'Test event #1')
        self.assertContains(response, 'Test event #2')


class UserProfileTest(CustomTestCase):

    def setUp(self):
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Test event #1', self.user_1)
        self.event_2 = self.create_event('Test event #2', self.user_2)
        # login
        self.client.login(username='user_1', password='test1234')

    def test_display_user_events(self):
        response = self.client.get(f'/{ self.user_1.username }')
        self.assertContains(response, 'Test event #1')
        self.assertNotContains(response, 'Test event #2')

    def test_display_other_user_events_readonly(self):
        response = self.client.get(f'/{ self.user_2.username }')
        self.assertContains(response, 'Test event #2')
        self.assertNotContains(response, 'Test event #1')
        self.assertNotContains(response, 'Edit')


class CreateEventViewTest(CustomTestCase):

    def post_data(self, title):
        return self.client.post(
            '/events/add',
            data={'title': title}
        )

    def setUp(self):
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        # login
        self.client.login(username='user_1', password='test1234')

    def test_displays_event_form(self):
        response = self.client.get('/events/add')
        self.assertIsInstance(response.context['form'], EventForm)

    def test_invalid_input_returns_form_to_template(self):
        response = self.post_data('a'*129)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EventForm)

    def test_invalid_input_returns_error_to_the_form_in_template(self):
        response = self.post_data('a'*129)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Ensure this value has at most 128 characters (it has 129).'
        )

    def test_invalid_input_doesnt_save_to_database(self):
        response = self.post_data('a'*129)
        self.assertEqual(Event.objects.count(), 0)

    def test_create_event_post(self):
        response = self.post_data('Test title #1')
        self.assertEqual(Event.objects.count(), 1)
        new_event = Event.objects.first()
        self.assertEqual(new_event.title, 'Test title #1')

    def test_redirect_after_post(self):
        response = self.post_data('Test title #1')
        self.assertRedirects(response, f'/{ self.user_1.username }')


class UpdateEventViewTest(CustomTestCase):

    def post_data(self, event_id, title):
        return self.client.post(
            f'/events/edit/{ event_id }',
            data={'title': title}
        )

    def setUp(self):
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Test event #1', self.user_1)
        self.event_2 = self.create_event('Test event #2', self.user_2)
        # login
        self.client.login(username='user_1', password='test1234')

    def test_displays_event_form(self):
        response = self.client.get(f'/events/edit/{ self.event_1.id }')
        self.assertIsInstance(response.context['form'], EventForm)

    def test_update_event_post(self):
        response = self.post_data(self.event_1.id, 'Test title #2')
        self.assertEqual(Event.objects.count(), 2)
        updated_event = Event.objects.first()
        self.assertEqual(updated_event.title, 'Test title #2')

    def test_redirect_after_post(self):
        response = self.post_data(self.event_1.id, 'Test title #2')
        self.assertRedirects(response, f'/{ self.user_1.username }')

    def test_cannot_update_other_users_event(self):
        response = self.post_data(self.event_2.id, 'Test title #3')
        self.assertEqual(response.status_code, 403)


class DeleteEventViewTest(CustomTestCase):

    def delete_post(self, event_id):
        return self.client.post(
            f'/events/delete/{ event_id }'
        )

    def setUp(self):
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Test event #1', self.user_1)
        self.event_2 = self.create_event('Test event #2', self.user_1)
        self.event_3 = self.create_event('Test event #3', self.user_2)
        # login
        self.client.login(username='user_1', password='test1234')

    def test_delete_event_get(self):
        response = self.client.get(
            f'/events/delete/{ self.event_1.id }'
        )
        self.assertEqual(Event.objects.count(), 3)
        first_event = Event.objects.first()
        self.assertEqual(first_event.title, 'Test event #1')
        self.assertEqual(response.context['event'], self.event_1)

    def test_delete_event_post(self):
        response = response = self.delete_post(self.event_1.id)
        self.assertEqual(Event.objects.count(), 2)
        first_event = Event.objects.first()
        self.assertEqual(first_event.title, 'Test event #2')

    def test_redirect_after_post(self):
        response = response = self.delete_post(self.event_1.id)
        self.assertRedirects(response, f'/{ self.user_1.username }')

    def test_cannot_delete_other_users_event(self):
        response = response = self.delete_post(self.event_3.id)
        self.assertEqual(response.status_code, 403)
