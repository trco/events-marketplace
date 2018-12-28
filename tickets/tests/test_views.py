from django.contrib.auth.models import User
# import form
from tickets.models import Ticket
from .base import CustomTestCase


class CreateTicketViewTest(CustomTestCase):

    def post_data(self, event_id, name):
        return self.client.post(
            f'/tickets/add/{ event_id }',
            data={'ticket_name': name}
        )

    def setUp(self):
        # create user
        self.user = self.create_user('user', 'test1234')
        # create event
        self.event = self.create_event('Test event #1', self.user)
        # login
        self.client.login(username='user', password='test1234')

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
        response = self.post_data(self.event.id, 'Test ticket')
        self.assertEqual(Ticket.objects.count(), 1)
        new_ticket = Ticket.objects.first()
        self.assertEqual(new_ticket.name, 'Test ticket')
        self.assertEqual(new_ticket.event_id, self.event.id)

    def test_redirect_after_post(self):
        response = self.post_data(self.event.id, 'Test ticket')
        self.assertRedirects(response, f'/{ self.user.username }')
