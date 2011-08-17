"""Group Form"""

import re
from pylons.i18n import ugettext as _
from tg import config, url
from tw.api import CSSLink
from tw.forms import TableForm, TextField, TextArea, CheckBox, Spacer, \
                     HiddenField, PasswordField, Label, SubmitButton, Button
from tw.forms.validators import Schema, Int, NotEmpty, UnicodeString, \
                                FieldsMatch, Email, URL        
                                
from dmirr.widgets.validators import UniqueEmail, UniqueGroupName, UserExists


class DynamicLabel(Label):
    value = ''
    template = 'dmirr.widgets.templates.dynamic_label' 
        
class GroupNewForm(TableForm):
    css = [CSSLink(link=url('/theme/%s/_css/group.css' % config['theme']))]
    validator = Schema(
        chained_validators=[
            UniqueGroupName(),
            ]
        )
    fields = [
        TextField('group_name', label_text='Group Name', help_text="This can not be changed.", 
            validator=UnicodeString(not_empty=True)),
        TextField('display_name', label_text='Display Name',
            validator=UnicodeString(not_empty=True)),
        Spacer(),
        ]
    submit_text = 'Register Group'
    
class GroupEditForm(TableForm):
    css = [CSSLink(link=url('/theme/%s/_css/group.css' % config['theme']))]
    validator = Schema(
        chained_validators=[
            UniqueGroupName(),
            ]
        )
    fields = [
        HiddenField('group_id', validator=Int()),
        HiddenField('group_name'),
        HiddenField('_method'),
        DynamicLabel('group_name', label_text='Group Name', suppress_label=False),
        TextField('display_name', label_text='Display Name',
            validator=UnicodeString(not_empty=True)),
        SubmitButton('submit', attrs=dict(value="Save Group")),
        Button('Cancel', attrs=dict(value="Cancel", onClick="history.back();"))
        ] 

class AddToGroupForm(TableForm):
    css = [CSSLink(link=url('/theme/%s/_css/group.css' % config['theme']))]
    validator = Schema(
        chained_validators=[
            UserExists()
            ]
        )
    fields = [
        HiddenField('group_id', validator=Int()),
        TextField('user_name', validator=UnicodeString(not_empty=True)),
        SubmitButton('submit', attrs=dict(value="Add User To Group")),
        ] 


create_group_form = GroupNewForm("create_group_form", action=url('/group'))
edit_group_form = GroupEditForm("edit_group_form", action=url('/group/?_method=PUT'))
add_to_group_form = AddToGroupForm("add_to_group_form", action=url('/group/assign_user'))