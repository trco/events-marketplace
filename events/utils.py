import urllib.parse
import urllib.request
from .GoogleMapsAPI import API_key


def getLatLon(address):
    # address should be utf8 encoded
    address = urllib.parse.quote(address.encode('utf8'))
    geo = urllib.request.urlopen(f'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address={ address }&key={ API_key }')
    return geo.read()
