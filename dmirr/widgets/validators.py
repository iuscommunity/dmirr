import re
import pylons
from pylons.i18n import ugettext as _
from formencode import Invalid
from formencode.schema import SimpleFormValidator
from tw.forms.validators import Email

from dmirr.model import DBSession as db
from dmirr import model

__all__ = ['UniqueEmail', 'UniqueUserName', 'UniqueGroupName']

def validate_unique_email(value_dict, state, validator):
    # first for edit forms
    if value_dict.has_key('user_id'):
        u1 = db.query(model.User).filter_by(user_id=value_dict['user_id'])\
             .first()
        if u1.email_address != value_dict['email_address']:
            u2 = db.query(model.User)\
                 .filter_by(email_address=value_dict['email_address']).first()
            if u2:
                return {'email_address':'The address already exists.'}
    # or new form                
    else:
        u1 = db.query(model.User)\
             .filter_by(email_address=value_dict['email_address']).first()
        if u1:
            return {'email_address':'The address already exists.'}
    

def validate_unique_user_name(value_dict, state, validator):
    # first for edit forms
    if value_dict.has_key('user_id'):
        u1 = db.query(model.User).filter_by(user_id=value_dict['user_id'])\
             .first()
        if u1 and u1.user_name != value_dict['user_name']:
            u2 = db.query(model.User)\
                 .filter_by(user_name=value_dict['user_name']).first()
            if u2:
                return {'user_name':'The user name already exists.'}
    # or new form        
    else:
        u1 = db.query(model.User)\
             .filter_by(user_name=value_dict['user_name']).first()
        if u1:
            return {'user_name':'The user name already exists.'}
   
def validate_user_exists(value_dict, state, validator):
    # first for edit forms
    if value_dict.has_key('user_name'):
        u = db.query(model.User).filter_by(user_name=value_dict['user_name'])\
             .first()
        if not u:
            return {'user_name':'%s does not exists.' % value_dict['user_name']}
    # or new form        
    else:
        return {'user_name':'User does not exists.'}
               
def validate_unique_group_name(value_dict, state, validator):
    # first for edit forms
    if value_dict.has_key('group_id'):
        g1 = db.query(model.Group).filter_by(group_id=value_dict['group_id'])\
             .first()
        if g1 and g1.group_name != value_dict['group_name']:
            g2 = db.query(model.Group)\
                 .filter_by(group_name=value_dict['gropu_name']).first()
            if g2:
                return {'group_name':'The group name already exists.'}
    # or new form                
    else:
        g1 = db.query(model.Group)\
             .filter_by(group_name=value_dict['group_name']).first()
        if g1:
            return {'group_name':'The group name already exists.'}
             
UserExists = SimpleFormValidator(validate_user_exists)
UniqueEmail = SimpleFormValidator(validate_unique_email)
UniqueUserName = SimpleFormValidator(validate_unique_user_name)
UniqueGroupName = SimpleFormValidator(validate_unique_group_name)
