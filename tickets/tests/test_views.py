from django.contrib.auth.models import User
from tickets.forms import TicketForm
from tickets.models import Ticket
from .base import CustomTestCase


class ManageTicketsViewTest(CustomTestCase):

    def post_data(self, event_id, name):
        return self.client.post(
            f'/tickets/{event_id}',
            data={'name': name}
        )

    def setUp(self):
        # create user
        self.user = self.create_user('user', 'test1234')
        # create event
        self.event = self.create_event('Test event #1', self.user)
        # login
        self.client.login(username='user', password='test1234')

    def test_displays_ticket_form(self):
        response = self.client.get(f'/tickets/{self.event.id}')
        self.assertIsInstance(response.context['form'], TicketForm)

    def test_invalid_input_returns_form_to_template(self):
        response = self.post_data(self.event.id, 'a'*129)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TicketForm)

    def test_invalid_input_returns_error_to_the_form_in_template(self):
        response = self.post_data(self.event.id, 'a'*129)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Ensure this value has at most 128 characters (it has 129).'
        )

    def test_invalid_input_doesnt_save_to_database(self):
        response = self.post_data(self.event, 'a'*129)
        self.assertEqual(Ticket.objects.count(), 0)

    def test_create_ticket_post(self):
        response = self.post_data(self.event.id, 'Test ticket #1')
        self.assertEqual(Ticket.objects.count(), 1)
        new_ticket = Ticket.objects.last()
        self.assertEqual(new_ticket.name, 'Test ticket #1')
        self.assertEqual(new_ticket.event_id, self.event.id)

    def test_redirect_after_post(self):
        response = self.post_data(self.event.id, 'Test ticket #1')
        self.assertRedirects(response, f'/tickets/{self.event.id}')


class DeleteTicketViewTest(CustomTestCase):

    def delete_post(self, ticket_id):
        return self.client.post(
            f'/tickets/delete/{ticket_id}'
        )

    def setUp(self):
        # create users
        self.user_1 = self.create_user('user_1', 'test1234')
        self.user_2 = self.create_user('user_2', 'test1234')
        # create events
        self.event_1 = self.create_event('Test event #1', self.user_1)
        self.event_2 = self.create_event('Test event #2', self.user_1)
        self.event_3 = self.create_event('Test event #3', self.user_2)
        # create events
        self.ticket_1 = self.create_ticket('Test ticket #1', self.event_1)
        self.ticket_2 = self.create_ticket('Test ticket #2', self.event_2)
        self.ticket_3 = self.create_ticket('Test ticket #3', self.event_3)
        # login
        self.client.login(username='user_1', password='test1234')

    def test_delete_ticket_get(self):
        response = self.client.get(
            f'/tickets/delete/{self.ticket_1.id}'
        )
        self.assertEqual(Ticket.objects.count(), 3)
        first_ticket = Ticket.objects.first()
        self.assertEqual(first_ticket.name, 'Test ticket #1')
        self.assertEqual(response.context['ticket'], self.ticket_1)

    def test_delete_ticket_post(self):
        response = self.delete_post(self.ticket_1.id)
        self.assertEqual(Ticket.objects.count(), 2)
        first_ticket = Ticket.objects.first()
        self.assertEqual(first_ticket.name, 'Test ticket #2')

    def test_redirect_after_post(self):
        response = self.delete_post(self.ticket_1.id)
        self.assertRedirects(response, f'/tickets/{self.event_1.id}')

    def test_cannot_delete_other_users_ticket(self):
        response = self.delete_post(self.ticket_3.id)
        self.assertEqual(response.status_code, 403)
