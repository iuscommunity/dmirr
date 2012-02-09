
from django import forms
from django.forms.widgets import HiddenInput
from guardian.shortcuts import assign, remove_perm

from dmirr.hub.forms import dMirrLabel
from dmirr.hub import db

ATTRS_DICT = {'class': 'required'}
LABEL_RE = r'^[a-zA-Z][\.\w\-]+$'
ERROR_MSG = 'Label must start with a letter and contain only letters, numbers, dashes, dots and underscores.'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = db.Project

    user = forms.ModelChoiceField(queryset=db.User.objects.all(), widget=HiddenInput)
    label = dMirrLabel()
                             
    def save(self):
        super(ProjectForm, self).save()
        assign('change_project', self.instance.user, self.instance)
        assign('delete_project', self.instance.user, self.instance)
        
        if self.instance.admin_group:
            assign('change_project', self.instance.admin_group, self.instance)
            assign('delete_project', self.instance.admin_group, self.instance)
        
        if self.initial.has_key('admin_group') and \
           self.initial['admin_group'] and 'admin_group' in self.changed_data:
            # means there was an admin group removed
            group = db.Group.objects.get(pk=self.initial['admin_group'])
            remove_perm('change_project', group, self.instance)
            remove_perm('delete_project', group, self.instance)
            
        return self.instance
    
class ProjectSecondaryForm(ProjectForm):
    def __init__(self, *args, **kwargs):
        super(ProjectSecondaryForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['admin_group'].required = False
            self.fields['admin_group'].widget.attrs['disabled'] = 'disabled'

    def clean_admin_group(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            try:
                self.changed_data.remove('admin_group')
            except ValueError, e:
                pass
            return instance.admin_group
        else:
            return self.cleaned_data.get('admin_group', None)

class ProjectRepoForm(forms.ModelForm):
    class Meta:
        model = db.ProjectRepo
        
    user = forms.ModelChoiceField(queryset=db.User.objects.all(), widget=HiddenInput)
    project = forms.ModelChoiceField(queryset=db.Project.objects.all(), widget=HiddenInput)
    label = dMirrLabel()