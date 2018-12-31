from tickets.forms import TicketForm
from tickets.models import Ticket
from .base import CustomTestCase


class CreateTicketFormTest(CustomTestCase):

    def setUp(self):
        # create user
        self.user = self.create_user('user', 'test1234')
        # create event
        self.event = self.create_event('Test event #1', self.user)
        # login
        self.client.login(username='user', password='test1234')

    def test_invalid_title_length(self):
        form = TicketForm(data={'name': 'a'*129})
        self.assertFalse(form.is_valid())

    def test_event_is_set_as_ticket_event_on_save(self):
        form = TicketForm(data={'name': 'Test ticket #1'})
        form.save(event=self.event)
        ticket = Ticket.objects.first()
        self.assertEqual(self.event, ticket.event)

    def test_form_handles_saving_to_database(self):
        form = TicketForm(data={'name': 'Test ticket #1'})
        new_ticket = form.save(event=self.event)
        ticket = Ticket.objects.first()
        self.assertEqual(new_ticket, ticket)
