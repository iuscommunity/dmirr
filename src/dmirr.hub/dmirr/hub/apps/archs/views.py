
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from dmirr.hub import db
from dmirr.hub.apps.archs.forms import ArchForm
from dmirr.hub.utils import ok, Http403, session_is_owner

def index(request):
    data = {}
    data['archs'] = db.Arch.objects.order_by('label').all()
    return render(request, 'archs/index.html', data)
    
@login_required
@ok('archs.create_arch')
def create(request):
    data = {}
    if request.method == 'POST':
        form = ArchForm(request.POST)
        if form.is_valid():
            arch = form.save()
            
            return redirect(reverse('archs_index'))
    else:
        form = ArchForm()
        
    data['form'] = form    
    return render(request, 'archs/create.html', data)

@login_required
@ok('archs.change_arch', (db.Arch, 'label', 'arch'))
def update(request, arch):
    data = {}
    arch = get_object_or_404(db.Arch, label=arch)

    if request.method == 'POST':
        form = ArchForm(request.POST, instance=arch)
        if form.is_valid():
            arch = form.save()
            return redirect(reverse('archs_index'))
    else:
        form = ArchForm(instance=arch)
        
    data['form'] = form   
    data['arch'] = arch 
    return render(request, 'archs/update.html', data)

def show(request, arch):
    data = {}
    data['arch'] = get_object_or_404(db.Arch, label=arch)
    return render(request, 'archs/show.html', data)

@login_required
@ok('archs.delete_arch', (db.Arch, 'label', 'arch'))
def delete(request, arch):
    data = {}
    arch = db.Arch.objects.get(label=arch)
    arch.delete()
    return redirect(reverse('archs_index'))
    
