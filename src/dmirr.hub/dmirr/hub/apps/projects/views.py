
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from dmirr.hub import db
from dmirr.hub.apps.projects.forms import ProjectForm
from dmirr.hub.utils import ok, Http403, session_is_owner


@login_required
def index(request):
    data = {}
    data['projects'] = db.Project.objects.by_session(request)
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
                                    kwargs={'project_id': project.id}))                                
    else:
        form = ProjectForm()
        
    data['form'] = form    
    return render(request, 'projects/create.html', data)

@login_required
@ok('projects.change_project', (db.Project, 'id', 'project_id'))
def update(request, project_id):
    data = {}
    project = db.Project.objects.get(pk=project_id)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            
            return redirect(reverse('show_project',
                                    kwargs={'project_id': project.id}))                                
    else:
        form = ProjectForm(instance=project)
        
    data['form'] = form   
    data['project'] = project 
    return render(request, 'projects/edit.html', data)

#@login_required
def show(request, project_id):
    data = {}
    data['project'] = db.Project.objects.get(pk=project_id)
    return render(request, 'projects/show.html', data)

@login_required
@ok('projects.delete_project', (db.Project, 'id', 'project_id'))
def delete(request, project_id):
    data = {}
    project = db.Project.objects.get(pk=project_id)
    project.delete()
    return redirect('/projects/')
    
