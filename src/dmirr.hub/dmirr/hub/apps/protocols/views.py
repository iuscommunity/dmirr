
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from dmirr.hub import db
from dmirr.hub.apps.protocols.forms import ProtocolForm
from dmirr.hub.utils import ok, Http403, session_is_owner

def list(request):
    data = {}
    data['protocols'] = db.Protocol.objects.order_by('label').all()
    return render(request, 'protocols/list.html', data)
    
@login_required
def manage(request):
    data = {}
    data['protocols'] = db.Protocol.objects.order_by('label').all()
    return render(request, 'protocols/manage.html', data)
    
@login_required
@ok('protocols.add_protocol')
def create(request):
    data = {}
    if request.method == 'POST':
        form = ProtocolForm(request.POST)
        if form.is_valid():
            protocol = form.save()
            
            return redirect(reverse('manage_protocols'))
    else:
        form = ProtocolForm()
        
    data['form'] = form    
    return render(request, 'protocols/create.html', data)

@login_required
@ok('protocols.change_protocol')
def update(request, protocol):
    data = {}
    protocol = get_object_or_404(db.Protocol, label=protocol)

    if request.method == 'POST':
        form = ProtocolForm(request.POST, instance=protocol)
        if form.is_valid():
            protocol = form.save()
            return redirect(reverse('manage_protocols'))
    else:
        form = ProtocolForm(instance=protocol)
        
    data['form'] = form   
    data['protocol'] = protocol 
    return render(request, 'protocols/update.html', data)

def show(request, protocol):
    data = {}
    data['protocol'] = get_object_or_404(db.Protocol, label=protocol)
    return render(request, 'protocols/show.html', data)

@login_required
@ok('protocols.delete_protocol')
def delete(request, protocol):
    data = {}
    protocol = db.Protocol.objects.get(label=protocol)
    protocol.delete()
    return redirect(reverse('manage_protocols'))
    
