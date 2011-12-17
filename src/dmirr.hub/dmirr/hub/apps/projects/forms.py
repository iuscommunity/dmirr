
from django.forms import ModelForm
from guardian.shortcuts import assign

from dmirr.hub import db

class ProjectForm(ModelForm):
    class Meta:
        model = db.Project
        exclude = ('groups',)

    def save(self):
        super(ProjectForm, self).save()
        assign('change_project', self.instance.user, self.instance)
        assign('delete_project', self.instance.user, self.instance)
        return self.instance