
from django import forms
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _
from userena.forms import SignupForm
from guardian.shortcuts import assign
from dmirr.hub import db

ATTRS_DICT = {'class': 'required'}
USERNAME_RE = r'^[a-zA-Z][\.\w]+$'
ERROR_MSG = 'Username must start with a letter and contain only letters, numbers, dots and underscores.'
class dMirrSignupForm(SignupForm):
    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=30,
                                widget=forms.TextInput(attrs=ATTRS_DICT),
                                label=_("Username"),
                                error_messages={'invalid': _(ERROR_MSG)})

class GroupForm(forms.ModelForm):
    #user = forms.ModelChoiceField(queryset=db.User.objects.all(), widget=HiddenInput)
    
    class Meta:
        model = db.Group
        exclude = ['permissions']
    
    def save(self):
        super(GroupForm, self).save()
        user = db.User.objects.get(username=self.data['user'])
        assign('change_group', user, self.instance)
        assign('delete_group', user, self.instance)
        self.instance.user_set.add(user)
        return self.instance
    