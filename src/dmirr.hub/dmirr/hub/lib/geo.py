
from django.conf import settings
from geopy import distance
import pygeoip
    
def get_geodata_by_ip(addr):
    gi = pygeoip.GeoIP(settings.GEO_CITY_FILE, pygeoip.MEMORY_CACHE)
    geodata = gi.record_by_addr(addr)
    return geodata

def get_distance(location1, location2):
    """
    Calculate distance between two locations, given the (lat, long) of each.
    
    Required Arguments:
    
        location1
            A tuple of (lat, long).
            
        location2
            A tuple of (lat, long).
            
    """
    return distance.distance(location1, location2).miles
    