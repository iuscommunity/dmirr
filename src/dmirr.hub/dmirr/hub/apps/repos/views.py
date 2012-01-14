
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from dmirr.hub import db
from dmirr.hub.apps.repos.forms import RepoForm
from dmirr.hub.utils import ok, Http403, session_is_owner

### NOTE: We check permissions on the project rather than the repo because
### users with perms on the project have full perms all the way down.

@login_required
def index(request, project):
    data = {}
    data['project'] = project = get_object_or_404(db.Project, label=project)
    data['repos'] = db.Repo.objects.filter(project=project)\
                      .order_by('label').all()
    return render(request, 'repos/index.html', data)
    
@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def create(request, project):
    data = {}
    project = get_object_or_404(db.Project, label=project)
    
    if request.method == 'POST':
        if not session_is_owner(request):
            return Http403
            
        form = RepoForm(request.POST)
        if form.is_valid():
            repo = form.save()
            
            return redirect(reverse('show_repo',
                                    kwargs=dict(repo=repo.label,
                                                project=repo.project.label)))
    else:
        form = RepoForm(initial=dict(
                            user=request.user,
                            project=project
                            ))
        
    data['form'] = form    
    data['project'] = project
    return render(request, 'repos/create.html', data)

@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def update(request, project, repo):
    data = {}
    repo = db.Repo.objects.get(label=repo)
    project = get_object_or_404(db.Project, label=project)
    
    if request.method == 'POST':
        form = RepoForm(request.POST, instance=repo)
        if form.is_valid():
            repo = form.save()
            
            return redirect(reverse('show_repo',
                                    kwargs=dict(repo=repo.label,
                                                project=repo.project.label)))
    else:
        form = RepoForm(instance=repo)
        
    data['form'] = form   
    data['repo'] = repo 
    data['project'] = project
    return render(request, 'repos/update.html', data)

#@login_required
def show(request, project, repo):
    data = {}
    data['project'] = get_object_or_404(db.Project, label=project)
    data['repo'] = get_object_or_404(db.Repo, label=repo)
    return render(request, 'repos/show.html', data)

@login_required
@ok('projects.change_project', (db.Project, 'label', 'project'))
def delete(request, project, repo):
    data = {}
    repo = db.Repo.objects.get(label=repo)
    repo.delete()
    return redirect(reverse('show_project',
                            kwargs=dict(project=repo.project.label)))
    
