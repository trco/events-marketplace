from django.test import TestCase
from tickets.models import Ticket


class TicketModelTest(TestCase):

    def test_create_read_ticket(self):
        # create tickets
        ticket_one = Ticket()
        ticket_one.name = 'Test ticket #1'
        ticket_one.save()

        ticket_two = Ticket()
        ticket_two.name = 'Test ticket #2'
        ticket_two.save()

        # read tickets
        tickets = Ticket.objects.all()
        self.assertEqual(tickets.count(), 2)

        saved_ticket_one = tickets[0]
        saved_ticket_two = tickets[1]

        self.assertIn('Test ticket #1', saved_ticket_one.name)
        self.assertIn('Test ticket #2', saved_ticket_two.name)
