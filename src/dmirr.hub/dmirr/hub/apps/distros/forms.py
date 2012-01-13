
from django import forms
from django.forms.widgets import HiddenInput
from guardian.shortcuts import assign

from dmirr.hub import db

class DistroForm(forms.ModelForm):
    class Meta:
        model = db.Distro
        
    user = forms.ModelChoiceField(queryset=db.User.objects.all(), widget=HiddenInput)
    project = forms.ModelChoiceField(queryset=db.Project.objects.all(), widget=HiddenInput)
    
    def save(self):
        super(DistroForm, self).save()
        assign('change_distro', self.instance.user, self.instance)
        assign('delete_distro', self.instance.user, self.instance)
        return self.instance