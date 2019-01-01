import json
from django.contrib.auth.models import User
from django.db import models
from .utils import getLatLon


class Event(models.Model):
    # relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # information
    title = models.CharField(max_length=128, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    # location
    address = models.CharField(max_length=256, blank=True, null=True)
    locality = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    # booleans
    active = models.BooleanField(blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True)
    # timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False, blank=True, null=True
    )

    def __str__(self):
            return self.title

    def save(self, *args, **kwargs):
        # save Event to get self.address for geocoding
        super(Event, self).save(*args, **kwargs)
        if self.address:
            # get locality, country, latitude & longitude from GoogleMaps API
            geo = json.loads(getLatLon(f'{ self.address }'))
            if geo['status'] == "OK":
                for item in geo['results'][0]['address_components']:
                    if item['types'][0] == 'postal_town':
                        self.locality = item['long_name']
                    elif item['types'][0] == 'locality':
                        self.locality = item['long_name']
                    elif item['types'][0] == 'country':
                        self.country = item['long_name']
                self.latitude = geo['results'][0]['geometry']['location']['lat']
                self.longitude = geo['results'][0]['geometry']['location']['lng']
