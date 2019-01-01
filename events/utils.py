import urllib.parse
import urllib.request
from django.conf import settings


def getLatLon(address):
    # address should be utf8 encoded
    address = urllib.parse.quote(address.encode('utf8'))
    geo = urllib.request.urlopen(f'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address={address}&key={settings.GOOGLE_MAPS_API_KEY}')
    return geo.read()
