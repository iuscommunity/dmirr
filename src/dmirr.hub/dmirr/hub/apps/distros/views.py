
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from dmirr.hub import db
from dmirr.hub.apps.distros.forms import DistroForm
from dmirr.hub.utils import ok, Http403, session_is_owner


@login_required
def index(request):
    data = {}
    data['distros'] = db.Distro.objects.all()
    return render(request, 'distros/index.html', data)
    
@login_required
def create(request):
    data = {}
    if request.method == 'POST':
        if not session_is_owner(request):
            return Http403
            
        form = DistroForm(request.POST)
        if form.is_valid():
            distro = form.save()
            
            return redirect(reverse('show_distro',
                                    kwargs={'distro_id': distro.id}))                                
    else:
        form = DistroForm()
        
    data['form'] = form    
    return render(request, 'distros/create.html', data)

@login_required
@ok('projects.change_project', (db.Distro, 'id', 'distro_id'))
def update(request, distro_id):
    data = {}
    distro = db.Distro.objects.get(pk=distro_id)
    
    if request.method == 'POST':
        form = DistroForm(request.POST, instance=distro)
        if form.is_valid():
            distro = form.save()
            
            return redirect(reverse('show_distro',
                                    kwargs={'distro_id': distro.id}))                                
    else:
        form = DistroForm(instance=distro)
        
    data['form'] = form   
    data['distro'] = distro 
    return render(request, 'distros/update.html', data)

#@login_required
def show(request, distro_id):
    data = {}
    data['distro'] = db.Distro.objects.get(pk=distro_id)
    return render(request, 'distros/show.html', data)

@login_required
@ok('distros.delete_distro', (db.Distro, 'id', 'distro_id'))
def delete(request, distro_id):
    data = {}
    distro = db.Distro.objects.get(pk=distro_id)
    distro.delete()
    return redirect('/distros/')
    
