
from django import forms
from django.utils.translation import ugettext_lazy as _
from userena.forms import SignupForm

ATTRS_DICT = {'class': 'required'}
USERNAME_RE = r'^[a-zA-Z][\.\w]+$'
ERROR_MSG = 'Username must start with a letter and contain only letters, numbers, dots and underscores.'
class dMirrSignupForm(SignupForm):
    username = forms.RegexField(regex=USERNAME_RE,
                                max_length=30,
                                widget=forms.TextInput(attrs=ATTRS_DICT),
                                label=_("Username"),
                                error_messages={'invalid': _(ERROR_MSG)})
