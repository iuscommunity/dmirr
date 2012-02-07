
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import HiddenInput
from guardian.shortcuts import assign

from dmirr.hub import db
from dmirr.hub.forms import dMirrLabel

ATTRS_DICT = {'class': 'required'}
LABEL_RE = r'[\.\w\d\-\_]+$'
ERROR_MSG = 'Label must start with a letter and contain only letters, numbers, dots, dashes, and underscores.'

class ProtocolForm(forms.ModelForm):
    class Meta:
        model = db.Protocol
        
    #label = forms.RegexField(regex=LABEL_RE,
    #                         max_length=30,
    #                         widget=forms.TextInput(attrs=ATTRS_DICT),
    #                         label=_("Label"),
    #                         error_messages={'invalid': _(ERROR_MSG)})
    label = dMirrLabel()