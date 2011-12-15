from django import forms
from django.forms import ModelForm
from guardian.shortcuts import assign
from nf import db
from django.forms.widgets import CheckboxSelectMultiple
from nf.apps.projects.models import ProjectShare

class ProjectForm(ModelForm):
    class Meta:
        model = db.Project
        #exclude = ('groups',)
