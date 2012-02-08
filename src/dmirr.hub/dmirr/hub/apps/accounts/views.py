
from django.shortcuts import redirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from dmirr.hub.apps.accounts.forms import GroupForm, AddUserToGroupForm
from dmirr.hub import db
from dmirr.hub.utils import ok, session_is_owner, Http403

def index_view(request):
    if request.user.is_authenticated():
        return redirect('/account/%s/' % request.user.username)
    else:
        return redirect('/account/signin/')
    
def my_projects(request, user):
    data = {}
    print request.user.profile.my_projects
    data['projects'] = request.user.profile.my_projects
    return render(request, 'accounts/projects.html', data)
    
@login_required
@ok('auth.change_user', (db.User, 'username', 'user'))
def show_api_key(request, user):
    data = {}
    user = get_object_or_404(db.User, username=user)
    data['profile'] = user.profile
    data['user'] = user
    return render(request, 'accounts/show_api_key.html', data)

@login_required
@ok('auth.change_user', (db.User, 'username', 'user'))
def reset_api_key(request, user):
    data = {}
    user = get_object_or_404(db.User, username=user)
    if user.api_key:
        user.api_key.key = user.api_key.generate_key()
        user.api_key.save()
    else:
        key = db.ApiKey(user=user)
        key.save()
        
    data['profile'] = user.profile
    data['user'] = user
    return redirect(reverse('show_api_key', kwargs={'user': user.username}))
    
def list_groups(request):
    data = {}
    data['groups'] = db.Group.objects.all()
    return render(request, 'accounts/groups/list.html', data)

@login_required
def manage_groups(request):
    data = {}
    return render(request, 'accounts/groups/manage.html', data)
    
@login_required
def create_group(request):
    data = {}

    if request.method == 'POST':
        post = request.POST.copy()
        post['user'] = request.user
        form = GroupForm(post)
        if form.is_valid():
            group = form.save()            
            return redirect(reverse('show_group', 
                                    kwargs=dict(group=group.id)))
    else:
        form = GroupForm()
        
    data['form'] = form
    return render(request, 'accounts/groups/create.html', data)
    
login_required
@ok('auth.change_group', (db.Group, 'pk', 'group'))
def update_group(request, group):
    data = {}
    group = db.Group.objects.get(pk=group)
    
    if request.method == 'POST':
        post = request.POST.copy()
        post['user'] = request.user
        form = GroupForm(post, instance=group)
        if form.is_valid():
            group = form.save()
            return redirect(reverse('show_group', 
                                    kwargs=dict(group=group.id)))
    else:
        form = GroupForm(instance=group)
        
    data['form'] = form   
    data['group'] = group 
    return render(request, 'accounts/groups/update.html', data)

@login_required
@ok('auth.change_group', (db.Group, 'id', 'group'))
def add_user_to_group(request, group):
    data = {}
    group = db.Group.objects.get(pk=group)    
    
    if request.method == 'POST':
        user = db.User.objects.get(pk=request.POST['user'])
        group.user_set.add(user)
        group.save()
        return redirect(reverse('show_group', kwargs=dict(group=group.id)))
        
    else:
        form = AddUserToGroupForm()
        data['form'] = form
        data['group'] = group 
        return render(request, 'accounts/groups/add.html', data)

@login_required
@ok('auth.change_group', (db.Group, 'pk', 'group'))
def remove_user_from_group(request, group):
    data = {}
    group = db.Group.objects.get(pk=group)    
    user = db.User.objects.get(username=request.GET['user'])

    group.user_set.remove(user)
    group.save()
    return redirect(reverse('show_group', kwargs=dict(group=group.id)))

        
def show_group(request, group):
    data = {}
    data['group'] = db.Group.objects.get(pk=group)
    return render(request, 'accounts/groups/show.html', data)

@login_required
@ok('auth.delete_group', (db.Group, 'pk', 'group'))
def delete_group(request, group):
    data = {}
    group = db.Group.objects.get(pk=group)
    group.delete()
    return redirect(reverse('groups_index'))
    