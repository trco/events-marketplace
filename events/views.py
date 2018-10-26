from django.shortcuts import redirect, render
from .models import Event


def index(request):
    context = {}
    events = Event.objects.all()
    context['events'] = events
    return render(request, 'events/index.html', context)


def create_event(request):
    context = {}

    if request.method == 'POST':
        event = Event.objects.create(title=request.POST.get('title_text'))
        return redirect('create_event')

    events = Event.objects.all()
    context['events'] = events

    return render(request, 'events/create_event.html', context)
