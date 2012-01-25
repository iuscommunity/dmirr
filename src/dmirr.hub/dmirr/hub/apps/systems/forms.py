
from django import forms
from django.forms.widgets import HiddenInput
from guardian.shortcuts import assign, remove_perm

from dmirr.hub import db

class SystemForm(forms.ModelForm):
    class Meta:
        model = db.System
        exclude = ['ip', 'longitude', 'latitude', 'country', 'city', 'region', 
                   'postal_code', 'country_code']
    
    user = forms.ModelChoiceField(queryset=db.User.objects.all(), widget=HiddenInput)
    label = forms.CharField(label="Hostname")

    def save(self):
        super(SystemForm, self).save()
        assign('change_system', self.instance.user, self.instance)
        assign('delete_system', self.instance.user, self.instance)
        
        if self.instance.admin_group:
            assign('change_system', self.instance.admin_group, self.instance)
            assign('delete_system', self.instance.admin_group, self.instance)
        
        if self.initial.has_key('admin_group') and \
           self.initial['admin_group'] and 'admin_group' in self.changed_data:
            # means there was an admin group removed
            group = db.Group.objects.get(pk=self.initial['admin_group'])
            remove_perm('change_system', group, self.instance)
            remove_perm('delete_system', group, self.instance)
            
        return self.instance