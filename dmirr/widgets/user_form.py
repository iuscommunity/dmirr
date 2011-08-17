"""User Form"""

import re
from pylons.i18n import ugettext as _
from tg import config, url
from tw.api import CSSLink
from tw.forms import TableForm, TextField, TextArea, CheckBox, Spacer, \
                     HiddenField, PasswordField, Label, SubmitButton, Button
from tw.forms.validators import Schema, Int, NotEmpty, UnicodeString, \
                                FieldsMatch, Email, URL        
                                
from dmirr.widgets.validators import UniqueEmail, UniqueUserName


class DynamicLabel(Label):
    value = ''
    template = 'dmirr.widgets.templates.dynamic_label' 
        
class UserNewForm(TableForm):
    css = [CSSLink(link=url('/theme/%s/_css/user.css' % config['theme']))]
    validator = Schema(
        chained_validators=[
            FieldsMatch('email_address', 'confirm_email'),
            FieldsMatch('password', 'confirm_password'),
            UniqueEmail(),
            UniqueUserName(),
            ]
        )
    fields = [
        TextField('user_name', label_text='User Name', help_text="This can not be changed.", 
            validator=UnicodeString(not_empty=True)),
        TextField('display_name', label_text='Display Name',
            validator=UnicodeString(not_empty=True)),
        TextField('web_url', label_text='Web URL',
            validator=URL(not_empty=False)),    
        Spacer(),
        TextField('email_address', label_text='Email Address',
            validator=Email(not_empty=True)),
        TextField('confirm_email', label_text='Confirm Email'),
        Spacer(),
        PasswordField('password', label_text='Password',
            validator=UnicodeString(not_empty=True)),
        PasswordField('confirm_password', label_text='Confirm Password'),
        Spacer(),
        TextArea('about', label_text='About/Description'),
        Spacer(),
        TextArea('terms', label_text='Terms of Use'),
        CheckBox('agreed_to_terms', label_text='Agree to Terms', 
            help_text="Check if you agree to the terms of use.",
            validator=NotEmpty),
        ]
    submit_text = 'Register User'
    
class UserEditForm(TableForm):
    css = [CSSLink(link=url('/theme/%s/_css/user.css' % config['theme']))]
    validator = Schema(
        chained_validators=[
            FieldsMatch('password', 'confirm_password'),
            UniqueEmail(),
            UniqueUserName(),
            ]
        )
    fields = [
        HiddenField('user_id', validator=Int()),
        HiddenField('user_name'),
        HiddenField('_method'),
        #TextField('user_name', label_text='User Name',  
        #    validator=UnicodeString(not_empty=True)),
        DynamicLabel('user_name', label_text="User Name", suppress_label=False),
        TextField('display_name', label_text='Display Name',
            validator=UnicodeString(not_empty=True)),
        TextField('web_url', label_text='Web URL',
            validator=URL(not_empty=False)), 
        TextField('email_address', label_text='Email Address',
            validator=Email(not_empty=True)),
        Spacer(),
        PasswordField('password', label_text='Password',
            validator=UnicodeString(not_empty=False)),
        PasswordField('confirm_password', label_text='Confirm Password'),
        Spacer(),
        TextArea('about', label_text='About/Description'),
        SubmitButton('submit', attrs=dict(value="Save User")),
        Button('Cancel', attrs=dict(value="Cancel", onClick="history.back();"))
        ] 

create_user_form = UserNewForm("create_user_form", action=url('/user/'))
edit_user_form = UserEditForm("edit_user_form", action=url('/user/?_method=PUT'))
