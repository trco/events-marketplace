from django.shortcuts import render


def index(request):
    return render(request, 'events/index.html')


def create_event(request):
    return render(request, 'events/create_event.html')
