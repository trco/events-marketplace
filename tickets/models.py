from django.db import models
from events.models import Event


class Ticket(models.Model):
    name = models.CharField(max_length=128)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
