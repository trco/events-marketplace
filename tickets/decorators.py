from django.core.exceptions import PermissionDenied
from .models import Ticket


def user_is_ticket_owner(function):
    def wrap(request, *args, **kwargs):
        ticket = Ticket.objects.get(pk=kwargs['ticket_id'])
        if ticket.event.user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
