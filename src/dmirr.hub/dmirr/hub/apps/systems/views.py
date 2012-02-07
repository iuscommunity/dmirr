
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from dmirr.hub import db
from dmirr.hub.apps.systems.forms import SystemForm, SystemResourceForm
from dmirr.hub.utils import ok, Http403, session_is_owner

### SYSTEMS
def index(request):
    data = {}
    data['systems'] = db.System.objects.order_by('label').all()
    return render(request, 'systems/index.html', data)
    
@login_required
def create(request):
    data = {}
    if request.method == 'POST':
        form = SystemForm(request.POST)
        if form.is_valid():
            system = form.save()
            
            return redirect(reverse('show_system', 
                            kwargs=dict(system=system.label)))
    else:
        form = SystemForm(initial=dict(user=request.user))
        
    data['form'] = form    
    return render(request, 'systems/create.html', data)

@login_required
@ok('systems.change_system', (db.System, 'label', 'system'))
def update(request, system):
    data = {}
    system = get_object_or_404(db.System, label=system)

    if request.method == 'POST':
        form = SystemForm(request.POST, instance=system)
        if form.is_valid():
            system = form.save()
            return redirect(reverse('show_system', 
                            kwargs=dict(system=system.label)))
    else:
        form = SystemForm(instance=system)
        
    data['form'] = form   
    data['system'] = system 
    return render(request, 'systems/update.html', data)

def show(request, system):
    data = {}
    data['system'] = get_object_or_404(db.System, label=system)
    return render(request, 'systems/show.html', data)

@login_required
@ok('systems.delete_system', (db.System, 'label', 'system'))
def delete(request, system):
    data = {}
    system = get_object_or_404(db.System, label=system)
    system.delete()
    return redirect(reverse('systems_index'))

### SYSTEM RESOURCES
    
@login_required
@ok('systems.change_system', (db.System, 'label', 'system'))
def create_resource(request, system):
    data = {}
    system = get_object_or_404(db.System, label=system)
    if request.method == 'POST':
        form = SystemResourceForm(request.POST)
        if form.is_valid():
            resource = form.save()
            
            return redirect(reverse('show_system', 
                            kwargs=dict(system=system.label)))
    else:
        form = SystemResourceForm(initial=dict(user=request.user,
                                               system=system))
        
    data['form'] = form    
    data['system'] = system
    return render(request, 'systems/resources/create.html', data)

@login_required
@ok('systems.change_system', (db.System, 'label', 'system'))
def update_resource(request, system, resource):
    data = {}
    system = get_object_or_404(db.System, label=system)
    resource = get_object_or_404(db.SystemResource, id=resource)
    if request.method == 'POST':
        form = SystemResourceForm(request.POST, instance=system)
        if form.is_valid():
            system = form.save()
            return redirect(reverse('show_system_resource', 
                            kwargs=dict(system=resource.id)))
    else:
        form = SystemResourceForm(instance=resource)
        
    data['form'] = form   
    data['resource'] = resource
    return render(request, 'systems/resources/update.html', data)

def show_resource(request, system, resource):
    data = {}
    data['resource'] = get_object_or_404(db.SystemResource, id=resource)
    return render(request, 'systems/resources/show.html', data)

@login_required
@ok('systems.delete_system', (db.System, 'label', 'system'))
def delete_resource(request, system, resource):
    data = {}
    system = get_object_or_404(db.System, label=system)
    resource = get_object_or_404(db.SystemResource, id=resource)
    resource.delete()
    return redirect(reverse('show_system', 
                            kwargs=dict(system=system.label)))
    
