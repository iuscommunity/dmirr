
from django import forms
from django.utils.translation import ugettext_lazy as _

ATTRS_DICT = {'class': 'required'}
LABEL_RE = r'[\.\w\d\-\_]+$'
ERROR_MSG = 'Label must start with a letter and contain only letters, numbers, dots, dashes, and underscores.'

class dMirrLabel(forms.RegexField):
    class Meta:
        regex = LABEL_RE
        max_length = 30
        widget = forms.TextInput(attrs=ATTRS_DICT)
        label = _("Label")
        error_messages = {'invalid': _(ERROR_MSG)}
    
    def __init__(self, *args, **kw):
        super(dMirrLabel, self).__init__(regex=LABEL_RE, *args, **kw)