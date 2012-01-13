
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from dmirr.hub import db
from dmirr.hub.apps.distros.forms import DistroForm
from dmirr.hub.utils import ok, Http403, session_is_owner

### NOTE: We check permissions on the project rather than the distro because
### users with perms on the project have full perms all the way down.

@login_required
def index(request, project):
    data = {}
    #data['distros'] = db.Distro.objects.filter(project__label=project)
    return render(request, 'distros/index.html', data)
    
@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def create(request, project):
    data = {}
    project = get_object_or_404(db.Project, label=project)
    
    if request.method == 'POST':
        if not session_is_owner(request):
            return Http403
            
        form = DistroForm(request.POST)
        if form.is_valid():
            distro = form.save()
            
            return redirect(reverse('show_distro',
                                    kwargs=dict(distro=distro.label,
                                                project=distro.project.label)))
    else:
        form = DistroForm(initial=dict(
                            user=request.user,
                            project=project
                            ))
        
    data['form'] = form    
    data['project'] = project
    return render(request, 'distros/create.html', data)

@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def update(request, project, distro):
    data = {}
    distro = db.Distro.objects.get(label=distro)
    project = get_object_or_404(db.Project, label=project)
    
    if request.method == 'POST':
        form = DistroForm(request.POST, instance=distro)
        if form.is_valid():
            distro = form.save()
            
            return redirect(reverse('show_distro',
                                    kwargs=dict(distro=distro.label,
                                                project=distro.project.label)))
    else:
        form = DistroForm(instance=distro)
        
    data['form'] = form   
    data['distro'] = distro 
    data['project'] = project
    return render(request, 'distros/update.html', data)

#@login_required
def show(request, project, distro):
    data = {}
    data['project'] = get_object_or_404(db.Project, label=project)
    data['distro'] = get_object_or_404(db.Distro, label=distro)
    return render(request, 'distros/show.html', data)

@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def delete(request, project, distro):
    data = {}
    distro = db.Distro.objects.get(label=distro)
    distro.delete()
    return redirect(reverse('show_project',
                            kwargs=dict(project=distro.project.label)))
    
