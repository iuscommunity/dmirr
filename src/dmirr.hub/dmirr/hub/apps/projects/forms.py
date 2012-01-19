
from django import forms
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import assign, remove_perm

from dmirr.hub import db

ATTRS_DICT = {'class': 'required'}
LABEL_RE = r'^[a-zA-Z][\.\w\-]+$'
ERROR_MSG = 'Label must start with a letter and contain only letters, numbers, dashes, dots and underscores.'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = db.Project

    user = forms.ModelChoiceField(queryset=db.User.objects.all(), widget=HiddenInput)
    label = forms.RegexField(regex=LABEL_RE,
                             max_length=30,
                             widget=forms.TextInput(attrs=ATTRS_DICT),
                             label=_("Label"),
                             error_messages={'invalid': _(ERROR_MSG)})
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