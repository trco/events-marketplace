from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title',)

    def save(self, user, *args, **kwargs):
        self.instance.user = user
        super().save(*args, **kwargs)
