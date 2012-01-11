
from django.forms import ModelForm
from guardian.shortcuts import assign

from dmirr.hub import db

class DistroForm(ModelForm):
    class Meta:
        model = db.Distro

#    def save(self):
#        super(DistroForm, self).save()
#        assign('change_distro', self.instance.user, self.instance)
#        assign('delete_distro', self.instance.user, self.instance)
#        return self.instance