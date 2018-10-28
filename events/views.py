from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Event


def index(request):
    context = {}
    events = Event.objects.all()
    context['events'] = events
    return render(request, 'events/index.html', context)


def login_redirection(request):
    return HttpResponseRedirect(reverse(
        'user_profile',
        args=[request.user.username])
    )


def user_profile(request, username=None):
    context = {}
    events = Event.objects.all()
    context['events'] = events
    return render(request, 'events/user_profile.html', context)


def create_update_event(request, event_id=None):
    context = {}

    if request.method == 'POST' and event_id is None:
        event = Event.objects.create(title=request.POST.get('title_text'))
        return redirect('create_event')
    elif request.method == 'POST' and event_id is not None:
        event = Event.objects.get(id=event_id)
        event.title = request.POST.get('title_text')
        event.save()
        return redirect('create_event')

    events = Event.objects.all()
    context['events'] = events

    return render(request, 'events/create_event.html', context)
