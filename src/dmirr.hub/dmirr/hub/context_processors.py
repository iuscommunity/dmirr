
from django.contrib.sites.models import Site
from pkg_resources import get_distribution

def template_shortcuts(request):
    from django.conf import settings
    cuts = {
        'baseurl' : settings.URL,
        'api' : "%s/%s" % (settings.URL, 'api/v0/'),
        'js' : '%sjs/' % settings.STATIC_URL,
        'img' : '%simg/' % settings.STATIC_URL,
        'css' : '%scss/' % settings.STATIC_URL,
        '3rdparty' : '%s3rdparty/' % settings.STATIC_URL,
        'site' : Site.objects.get_current(),
        'dmirr_version' : get_distribution('dmirr.hub').version,
        'flags' : "%simg/flags/" % settings.STATIC_URL,
        'google_maps_key' : settings.GOOGLE_MAPS_KEY,
        }
    return cuts