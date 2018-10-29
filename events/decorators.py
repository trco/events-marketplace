from django.core.exceptions import PermissionDenied
from .models import Event


def user_is_event_owner(function):
    def wrap(request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs['event_id'])
        if event.user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
