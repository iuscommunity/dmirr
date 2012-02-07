
from django import forms
from django.forms.widgets import HiddenInput
from guardian.shortcuts import assign

from dmirr.hub import db
from dmirr.hub.forms import dMirrLabel

class ArchForm(forms.ModelForm):
    class Meta:
        model = db.Arch
    label = dMirrLabel()