from django import forms
from haystack.forms import SearchForm
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title', 'address')

    def save(self, *args, user=None, **kwargs):
        if user is not None:
            self.instance.user = user
        return super().save(*args, **kwargs)


class SearchEventsForm(SearchForm):
    q = forms.CharField(max_length=256, required=False)
