
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from dmirr.hub import db
from dmirr.hub.apps.projects.forms import ProjectForm, ProjectSecondaryForm
from dmirr.hub.apps.projects.forms import ProjectRepoForm
from dmirr.hub.utils import ok, Http403, session_is_owner

def list(request):
    data = {}
    data['projects'] = db.Project.objects.order_by('label').all()
    return render(request, 'projects/list.html', data)

@login_required
def manage(request):
    data = {}
    data['projects'] = request.user.profile.projects
    return render(request, 'projects/manage.html', data)
    
@login_required
@ok('projects.add_project')
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

    form.fields['admin_group'].queryset = request.user.profile\
                                                 .managed_groups.all()    
    data['form'] = form    
    return render(request, 'projects/create.html', data)

@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def update(request, project):
    data = {}
    project = get_object_or_404(db.Project, label=project)
    
    if request.method == 'POST':
        if request.user == project.user:
            form = ProjectForm(request.POST, instance=project)
        else:
            form = ProjectSecondaryForm(request.POST, instance=project)
            
        if form.is_valid():
            project = form.save()
            return redirect(reverse('show_project',
                                    kwargs={'project': project.label}))                                
    else:
        if request.user == project.user:
            form = ProjectForm(instance=project)
            form.fields['admin_group'].queryset = request.user.profile\
                                                         .managed_groups.all()    
        else:
            form = ProjectSecondaryForm(
                instance=project,            
                initial=dict(admin_group=project.admin_group),
                )

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
    project = get_object_or_404(db.Project, label=project)
    project.delete()
    return redirect('/projects/')
    
### REPOS

@login_required
def list_repos(request, project):
    data = {}
    data['project'] = project = get_object_or_404(db.Project, label=project)
    data['repos'] = db.ProjectRepo.objects.filter(project=project)\
                      .order_by('label').all()
    return render(request, 'projects/repos/list.html', data)
    
@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def create_repo(request, project):
    data = {}
    project = get_object_or_404(db.Project, label=project)
    
    if request.method == 'POST':
        if not session_is_owner(request):
            return Http403
            
        form = ProjectRepoForm(request.POST)
        if form.is_valid():
            repo = form.save()
            
            return redirect(reverse('show_project',
                                    kwargs=dict(project=repo.project.label)))
    else:
        form = ProjectRepoForm(initial=dict(
                            user=request.user,
                            project=project
                            ))
        
    data['form'] = form    
    data['project'] = project
    return render(request, 'projects/repos/create.html', data)

@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def update_repo(request, project, repo):
    data = {}
    repo = db.ProjectRepo.objects.get(label=repo)
    project = get_object_or_404(db.Project, label=project)
    
    if request.method == 'POST':
        form = ProjectRepoForm(request.POST, instance=repo)
        if form.is_valid():
            repo = form.save()
            
            return redirect(reverse('show_project',
                                    kwargs=dict(project=repo.project.label)))
    else:
        form = ProjectRepoForm(instance=repo)
        
    data['form'] = form   
    data['repo'] = repo 
    data['project'] = project
    return render(request, 'projects/repos/update.html', data)

#@login_required
def show_repo(request, project, repo):
    data = {}
    data['project'] = get_object_or_404(db.Project, label=project)
    data['repo'] = get_object_or_404(db.ProjectRepo, label=repo)
    return render(request, 'projects/repos/show.html', data)

@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def delete_repo(request, project, repo):
    data = {}
    repo = db.ProjectRepo.objects.get(label=repo)
    repo.delete()
    return redirect(reverse('show_project',
                            kwargs=dict(project=repo.project.label)))
    
