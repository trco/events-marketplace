from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from events.models import Event
from tickets.models import Ticket


@login_required
def create_ticket(request, event_id):
    context = {}

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        Ticket.objects.create(
            name=request.POST['ticket_name'],
            event_id=event_id
        )
        return HttpResponseRedirect(
            reverse('user_profile',  args=[request.user.username])
        )

    context['event'] = event

    return render(request, 'tickets/create_update_ticket.html', context)
