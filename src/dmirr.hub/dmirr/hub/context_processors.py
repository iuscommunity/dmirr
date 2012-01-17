
from django.contrib.sites.models import Site
from pkg_resources import get_distribution

def template_shortcuts(request):
    from django.conf import settings
    cuts = {
        'baseurl' : settings.URL,
        'api' : "%s/%s" % (settings.URL, 'api/v0/'),
        'js' : '%sjs/' % settings.STATIC_URL,
        'img' : '%simages/' % settings.STATIC_URL,
        'css' : '%scss/' % settings.STATIC_URL,
        '3rdparty' : '%s3rdparty/' % settings.STATIC_URL,
        'site' : Site.objects.get_current(),
        'dmirr_version' : get_distribution('dmirr.hub').version
        }
    return cuts