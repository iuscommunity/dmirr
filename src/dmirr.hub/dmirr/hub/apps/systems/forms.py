
from django import forms
from django.forms.widgets import HiddenInput
from guardian.shortcuts import assign, remove_perm

from dmirr.hub import db

class SystemForm(forms.ModelForm):
    class Meta:
        model = db.System
        exclude = ['ip', 'longitude', 'latitude',
                   'postal_code', 'country_code', 'online']
    
    user = forms.ModelChoiceField(queryset=db.User.objects.all(), widget=HiddenInput)
    label = forms.CharField(label="Hostname")

    def __init__(self, *args, **kwargs):
        super(SystemForm, self).__init__(*args, **kwargs)
        self.fields['country'].required = False
        self.fields['city'].required = False
        self.fields['region'].required = False

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

class SystemSecondaryForm(SystemForm):
    def __init__(self, *args, **kwargs):
        super(SystemSecondaryForm, self).__init__(*args, **kwargs)
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
                    
class SystemResourceForm(forms.ModelForm):
    class Meta:
        model = db.SystemResource
    
    user = forms.ModelChoiceField(queryset=db.User.objects.all(), widget=HiddenInput)
    system = forms.ModelChoiceField(queryset=db.System.objects.all(), widget=HiddenInput)
    
    def save(self):
        self.instance.path = "/%s/" % self.instance.path.lstrip('/').rstrip('/')
        return super(SystemResourceForm, self).save()
        
