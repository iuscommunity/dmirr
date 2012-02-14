
import re
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from dmirr.hub.lib.geo import get_geodata_by_ip, get_distance
from dmirr.hub import db

def get_location(city=None, region=None, country=None):
    if city and region and country:
        location = "%s, %s %s" % (city, region, country)
    elif region and country:
        location = "%s %s" % (region, country)
    elif country:
        location = country
    else:
        location = 'US'
    return location

def mirrorlist(request):
    data = {}
    resources = []
    remote = request.environ[settings.DMIRR_REMOTE_ADDR_KEY]
    
    client = get_geodata_by_ip(remote)
    repo = get_object_or_404(db.ProjectRepo, 
                             label=request.GET.get('repo', None))
    arch = get_object_or_404(db.Arch, 
                             label=request.GET.get('arch', None))
    protocol = get_object_or_404(db.Protocol, 
                             label=request.GET.get('protocol', 'http'))
    
    key = "%s-%s-%s-%s" % (remote, repo.id, arch.id, protocol.id)

    cached_data = cache.get(key)
    if cached_data:
        data = cached_data
    else:
        for resource in repo.project.resources.all():
            if not resource.include_in_mirrorlist:
                continue
            if protocol in resource.protocols.all() and \
               arch in repo.archs.all():
                full_uri = "%s://%s/%s/%s/" % (
                    protocol.label, 
                    resource.system.label,
                    resource.path.strip('/'),
                    re.sub('@arch@', arch.label, repo.path.strip('/')),
                    )
                if not client:
                    distance = 'unknown'
                else:
                    distance = get_distance( 
                        (client['latitude'], client['longitude']), 
                        (resource.system.latitude, resource.system.longitude),
                        )
                resources.append((distance, full_uri, resource))
            
        resources.sort()
        if not client:
            data['location'] = 'Unknown Location (%s)' % remote
        else:
            loc = get_location(client.get('city', None), 
                               client.get('region_name', None), 
                               client.get('country_name', None))
            data['location'] = '%s (%s)' % (loc, remote)
            
        data['resources'] = resources
        cache.set(key, data)
        
    return render(request, 'mirrorlist/list.html', data, 
                  content_type='text/plain')

