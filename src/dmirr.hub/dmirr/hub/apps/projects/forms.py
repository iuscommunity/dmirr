
from django.forms import ModelForm

from dmirr.hub import db

class ProjectForm(ModelForm):
    class Meta:
        model = db.Project
        exclude = ('groups',)
