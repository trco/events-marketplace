from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from events.models import Event
from .decorators import user_is_ticket_owner
from .forms import TicketForm
from .models import Ticket


@login_required
def manage_tickets(request, event_id):
    context = {}

    event = get_object_or_404(Event, id=event_id)
    tickets = Ticket.objects.filter(event_id=event_id)

    form = TicketForm(request.POST or None)

    if form.is_valid():
        form.save(event=event)
        return HttpResponseRedirect(
            reverse('manage_tickets',  args=[event_id])
        )

    context['form'] = form
    context['event'] = event
    context['tickets'] = tickets

    return render(request, 'tickets/manage_tickets.html', context)


@login_required
@user_is_ticket_owner
def delete_ticket(request, ticket_id):
    context = {}
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        ticket.delete()
        return HttpResponseRedirect(
            reverse('manage_tickets', args=[ticket.event_id])
        )

    context['ticket'] = ticket

    return render(request, 'tickets/delete_ticket.html', context)
