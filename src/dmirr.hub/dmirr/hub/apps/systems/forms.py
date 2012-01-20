
from django import forms
from django.forms.widgets import HiddenInput
from guardian.shortcuts import assign

from dmirr.hub import db

class SystemForm(forms.ModelForm):
    class Meta:
        model = db.System
        exclude = ['ip', 'longitude', 'latitude', 'country', 'city', 'region', 
                   'postal_code', 'country_code']
    
    label = forms.CharField(label="Hostname")