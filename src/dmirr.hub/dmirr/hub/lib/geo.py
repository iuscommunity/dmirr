
from django.conf import settings
import pygeoip
    
def get_geodata_by_ip(addr):
    gi = pygeoip.GeoIP(settings.GEO_CITY_FILE, pygeoip.MEMORY_CACHE)
    geodata = gi.record_by_addr(addr)
    return geodata

    