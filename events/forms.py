from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title',)

    def save(self, *args, user=None, **kwargs):
        if user is not None:
            self.instance.user = user
        return super().save(*args, **kwargs)
