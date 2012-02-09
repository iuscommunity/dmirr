
from django import forms
from dmirr.hub.forms import dMirrLabel
from dmirr.hub import db

class ProtocolForm(forms.ModelForm):
    class Meta:
        model = db.Protocol

    label = dMirrLabel()