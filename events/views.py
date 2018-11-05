from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .decorators import user_is_event_owner
from .models import Event


def index(request):
    context = {}
    events = Event.objects.all()
    context['events'] = events

    return render(request, 'events/index.html', context)


@login_required
def user_profile(request, username=None):
    context = {}
    events = Event.objects.filter(user__username=username)
    context['events'] = events

    return render(request, 'events/user_profile.html', context)


@login_required
def create_event(request):
    if request.method == 'POST':
        event = Event.objects.create(
            title=request.POST.get('title_text'),
            user_id=request.POST.get('user_id')
        )
        return HttpResponseRedirect(reverse(
            'user_profile',
            args=[request.user.username])
        )

    context = {}
    events = Event.objects.all()
    context['events'] = events

    return render(request, 'events/create_update_event.html', context)


@login_required
@user_is_event_owner
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.title = request.POST.get('title_text')
        event.save()
        return HttpResponseRedirect(reverse(
            'user_profile',
            args=[request.user.username])
        )

    context = {}
    context['event'] = event

    return render(request, 'events/create_update_event.html', context)


@login_required
@user_is_event_owner
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        return HttpResponseRedirect(reverse(
            'user_profile',
            args=[request.user.username])
        )

    context = {}
    context['event'] = event

    return render(request, 'events/delete_event.html', context)
