from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('name',)

    def save(self, *args, event=None, **kwargs):
        if event is not None:
            self.instance.event = event
        return super().save(*args, **kwargs)
