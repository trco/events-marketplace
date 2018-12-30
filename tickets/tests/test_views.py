from django.contrib.auth.models import User
# import form
from tickets.models import Ticket
from .base import CustomTestCase


class ManageTicketsViewTest(CustomTestCase):

    def post_data(self, event_id, name):
        return self.client.post(
            f'/tickets/{ event_id }',
            data={'ticket_name': name}
        )

    def setUp(self):
        # create user
        self.user = self.create_user('user', 'test1234')
        # create event
        self.event = self.create_event('Test event #1', self.user)
        # create ticket
        self.ticket = self.create_ticket('Test ticket #1', self.event)
        # login
        self.client.login(username='user', password='test1234')

    def test_manage_tickets_get(self):
        response = self.client.get(f'/tickets/{ self.event.id }')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test ticket #1')

    """
    def test_displays_ticket_form(self):
        response = self.client.get('/ticket/add')
        self.assertIsInstance(response.context['form'], TicketForm)

    def test_invalid_input_returns_form_to_template(self):
        response = self.post_data('a'*129)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TicketForm)

    def test_invalid_input_returns_error_to_the_form_in_template(self):
        response = self.post_data('a'*129)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'Ensure this value has at most 128 characters (it has 129).'
        )

    def test_invalid_input_doesnt_save_to_database(self):
        response = self.post_data('a'*129)
        self.assertEqual(Ticket.objects.count(), 0)
    """

    def test_create_ticket_post(self):
        response = self.post_data(self.event.id, 'Test ticket #2')
        self.assertEqual(Ticket.objects.count(), 2)
        new_ticket = Ticket.objects.last()
        self.assertEqual(new_ticket.name, 'Test ticket #2')
        self.assertEqual(new_ticket.event_id, self.event.id)

    def test_redirect_after_post(self):
        response = self.post_data(self.event.id, 'Test ticket #2')
        self.assertRedirects(response, f'/tickets/{ self.event.id }')
