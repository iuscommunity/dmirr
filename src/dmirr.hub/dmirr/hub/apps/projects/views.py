
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from dmirr.hub import db
from dmirr.hub.apps.projects.forms import ProjectForm
from dmirr.hub.utils import ok, Http403, session_is_owner

def index(request):
    data = {}
    data['projects'] = db.Project.objects.order_by('label').all()
    return render(request, 'projects/index.html', data)
    
@login_required
def create(request):
    data = {}
    if request.method == 'POST':
        if not session_is_owner(request):
            return Http403
            
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            
            return redirect(reverse('show_project',
                                    kwargs={'project': project.label}))                                
    else:
        form = ProjectForm(initial=dict(user=request.user))
        
    data['form'] = form    
    return render(request, 'projects/create.html', data)

@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def update(request, project):
    data = {}
    project = db.Project.objects.get(label=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            
            return redirect(reverse('show_project',
                                    kwargs={'project': project.label}))                                
    else:
        form = ProjectForm(instance=project)
        
    data['form'] = form   
    data['project'] = project 
    return render(request, 'projects/update.html', data)

def show(request, project):
    data = {}
    data['project'] = db.Project.objects.get(label=project)
    return render(request, 'projects/show.html', data)

@login_required
@ok('projects.delete_project', (db.Project, 'label', 'project'))
def delete(request, project):
    data = {}
    project = db.Project.objects.get(label=project)
    project.delete()
    return redirect('/projects/')
    
