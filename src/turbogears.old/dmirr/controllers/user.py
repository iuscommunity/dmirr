# -*- coding: utf-8 -*-
"""user controller with all its actions protected."""
import re
from tg import expose, validate, flash, url, request, redirect, config, \
               require, tmpl_context

from repoze.what.predicates import Any, is_user, has_permission, not_anonymous
import transaction
import pylons
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from repoze.what.predicates import has_permission
from formencode import validators
from tg.exceptions import HTTPNotFound
from tg.controllers import RestController
import turbomail

from dmirr import model as model
from dmirr.model import DBSession as db
from dmirr.lib import helpers as _h
from dmirr.lib.exc import *
from dmirr.widgets.user_form import create_user_form, edit_user_form



__all__ = ['UserController']
TERMS_OF_USE=open(config['terms_of_use_file']).read()

EMAIL_VERIFICATION_MSG = """
dMirr Email Verification

Registration for %s has begun, but you're not finished yet! You
first need to click the link below to verify your email address:

Click This Link: %s

---
If you did not register this email address on %s
please do NOT click the above link!
"""

WELCOME_MSG = """
Welcome To dMirr

Your account for %s has been successfully created and verified.  

username: %s
password: ************

---
%s
"""

CHANGE_EMAIL_VERIFICATION_MSG = """
dMirr Email Verification

An email change request was received for %s! To complete the change
you need to click the link below to verify your email address:

Click This Link: %s

---
If you did not request an email address change on %s
please do NOT click the above link!
"""


PASSWORD_RESET_MSG = """
dMirr Password Reset

Per your request, we have reset the password for %s.  Please login now and
change your password to something that you will remember.

username: %s
password: %s

---
%s
"""

class UserController(RestController):
    def _strip_private(self, user_obj):
        # instantiate objects
        user_obj.groups
        user_obj.permissions
        
        if request.identity:
            if user_obj.user_id == request.identity['user'].user_id \
                or 'dmirr_admin' in request.identity['user'].groups:
                pass
            else:
                del user_obj.verify_code
                del user_obj.email_address
                del user_obj._password
        else:
            del user_obj.verify_code
            del user_obj.email_address
            del user_obj._password
        return user_obj
            
    @expose('json')
    @expose('dmirr.templates.%s.user.get_one' % config['theme'])
    def get_one(self, user_name=None, *a, **kw):
        u = db.query(model.User).filter_by(user_name=user_name).first()
        new_u = self._strip_private(u)
        return dict(page='user', errors={}, user=new_u)
        
    @expose('json')
    @expose('dmirr.templates.%s.generic_get_all' % config['theme'])
    def get_all(self, *a, **kw):
        protected_users = []
        users = db.query(model.User).all()
        for u in users:
            protected_users.append(self._strip_private(u))
        return dict(errors={}, page='user', page_title="dMirr Users",
                    users=protected_users)
        
    @expose('dmirr.templates.%s.generic_new_form' % config['theme'])
    def new(self, *a, **kw):
        if config['user_registration'] == 'closed':
            flash(_('User registration is currently closed'), 'warning')
            redirect(url('/'))
            
        errors = _h.get_validation_errors()
        tmpl_context.form = create_user_form
        return dict(page='user', page_title='New User Registration', 
                    errors=errors, terms_of_use=TERMS_OF_USE)


    @expose('dmirr.templates.%s.generic_edit_form' % config['theme'])
    def edit(self, user_name=None, **kw):
        user = db.query(model.User).filter_by(user_name=user_name).first()
        if not user:
            raise HTTPNotFound
        
        _h.protect_user_obj(user)
            
        errors = _h.get_validation_errors()
        tmpl_context.form = edit_user_form
        return dict(page='user', page_title='Edit Account Settings', 
                    errors=errors, user=user)

    @expose('json')
    @expose('dmirr.templates.%s.generic_new_form' % config['theme'])
    def process_new_form_errors(self, *args, **kw):
        if pylons.request.response_type == 'application/json':
            kw['errors'] = pylons.tmpl_context.form_errors
            return dict(kw)
        else:
            errors = _h.get_validation_errors()
            tmpl_context.form = create_user_form
            return dict(page='user', page_title='New User Registration', 
                        errors=errors, terms_of_use=TERMS_OF_USE)

    @expose('json')
    @expose('dmirr.templates.%s.generic_edit_form' % config['theme'])
    def process_edit_form_errors(self, *args, **kw):
        if pylons.request.response_type == 'application/json':
            kw['errors'] = pylons.tmpl_context.form_errors
            return dict(kw)
        else:
            user = db.query(model.User).filter_by(user_id=kw['user_id']).first()
            _h.protect_user_obj(user)
            
            #errors = _h.get_validation_errors()
            tmpl_context.form = edit_user_form
            return dict(page='user', page_title='Edit Account Settings', 
                        user=user)
        
    @expose('json')
    @validate(create_user_form, error_handler=process_new_form_errors)
    def post(self, **kw):
        if config['user_registration'] == 'closed':
            abort(500)
            
        errors = _h.get_validation_errors()
                      
        u = model.User()
        u.user_name = unicode(re.sub(' ', '_', kw['user_name']).lower())
        u.display_name = unicode(kw['display_name'])
        u.web_url = unicode(kw['web_url'])
        u.email_address = unicode(kw['email_address'])
        u.about = kw['about']
        u.agreed_to_terms = int(1)
        u.status = _h.status_by_name('PendingEmailVerification')
        u.password = kw['password']
        
        # add to the everyone group
        everyone = _h.group_by_name('dmirr_everyone')
        everyone.users.append(u)     
        
        msg = turbomail.Message(
            config['from_email'],
            u.email_address,
            "dMirr Email Verification"
            )
        u.verify_code = _h.gen_verification_code()
        _url = "%s/user/true_up?u=%s&vc=%s" % (config['base_url'], 
                                              u.user_name, u.verify_code)
        msg.plain = EMAIL_VERIFICATION_MSG % \
                    (u.display_name, _url, config['base_url'])
        
        db.add(u)
        transaction.commit()
        msg.send()
        flash(_('%s registration started, check email to complete.' \
                % kw['display_name']), 'info')
        redirect(url('/'))

    @expose('json')
    @validate(edit_user_form, error_handler=edit)
    def put(self, *a, **kw):
        u = db.query(model.User).filter_by(user_id=kw.get('user_id', None))\
            .first()
        if not u:
            raise HTTPNotFound
                            
        _h.protect_user_obj(u)
        
        u.user_name = unicode(re.sub(' ', '_', kw['user_name']).lower())
        u.display_name = unicode(kw['display_name'])
        u.web_url = unicode(kw['web_url'])
        u.about = kw['about']
        
        if kw['password'] != 'xxxxxxxxxxxx':
            u.password = kw['password']
        
        if u.email_address != kw['email_address']:    
            msg = turbomail.Message(
                config['from_email'],
                kw['email_address'],
                "dMirr Email Verification"
                )
            u.verify_code = _h.gen_verification_code()
            _url = "%s/user/change_email?u=%s&e=%s&vc=%s" % (
                config['base_url'], u.user_name, kw['email_address'],
                u.verify_code
                )
            msg.plain = CHANGE_EMAIL_VERIFICATION_MSG % \
                        (u.display_name, _url, config['base_url'])
        
            msg.send()
            transaction.commit()
            
            flash(_("%s's settings have been saved.  Email change verification sent via email." % kw['display_name']), 
                    'info')
        else:
            transaction.commit()
            flash(_("%s's settings have been saved." % kw['display_name']), 
                    'info')
        redirect(url('/dashboard'))
    
    @expose()
    @validate(validators={
        "u": validators.UnicodeString(not_empty=True),
        "vc": validators.UnicodeString(not_empty=True) })
    def true_up(self, **kw):
        errors = _h.get_validation_errors()
        u = db.query(model.User).filter_by(user_name=kw['u'])\
            .filter_by(verify_code=kw['vc']).first()

        if not u:
            flash(_('%s was not found or invalid code!' % kw['u']), 'warning')
            redirect(url('/login'))

        u.status = _h.status_by_name('Enabled')
        flash(_('%s successfully verified! You can now login!' % u.email_address), 'info')

        # the email           
        msg = turbomail.Message(
            config['from_email'],
            u.email_address,
            "Welcome To dMirr"
            )
        msg.plain = WELCOME_MSG % (u.display_name, u.user_name, config['base_url'])

        transaction.commit()
        msg.send()

        redirect(url('/login'))
    
    @expose()
    @validate(validators={
        "u": validators.UnicodeString(not_empty=True),
        "e": validators.Email(not_empty=True),
        "vc": validators.String(not_empty=True) })
    def change_email(self, **kw):
        u = db.query(model.User).filter_by(user_name=kw['u'])\
            .filter_by(verify_code=kw['vc']).first()

        if not u:
            flash(_('Email verification failed.  %s was not found or invalid code!' % kw['u']), 'warning')
            redirect(url('/dashboard'))

        u.email_address = kw['e']
        db.flush()
        flash(_('%s successfully changed email address to %s!' % (u.display_name, u.email_address)),
'info')
        transaction.commit()

        redirect(url('/dashboard'))
    
    @validate(validators={
        "e": validators.Email(not_empty=True),
        "vc": validators.String(not_empty=True) })
    def reset_pwd(self, **kw):
        u = DBSession.query(User).filter_by(email_address=kw['e'])\
            .filter_by(verify_code=kw['vc'])\
            .first()
        if not u:
            flash(_('Invalid email address or verification code!'), 'warn')
            redirect(url('/'))

        new_pass = _h.gen_password()
        u.password = new_pass

        # the email           
        msg = turbomail.Message(
            "noreply@neighborfarms.org",
            u.email_address,
            "Neighbor Farms Password Reset"
            )
        msg.plain = PASSWORD_RESET_MSG % (u.display_name, u.email_address, new_pass, config['base_url'])

        DBSession.flush()
        transaction.commit()
        msg.send()

        flash(_("You're password has been reset, and sent via email."), 'info')
        redirect(url('/login'))
    
    @require(not_anonymous(msg="Must be logged in."))
    @expose('dmirr.templates.%s.delete_wrapper' % config['theme'])
    def delete(self, user_name=None, *a, **kw):
        u = db.query(model.User).filter_by(user_name=user_name).first()
        admins = db.query(model.Group).filter_by(group_name='dmirr_admin')\
                 .all()

        _display_name = u.display_name
        if not u:
            raise HTTPNotFound
        
        _h.protect_user_obj(u)
        
        came_from = url('/user/%s/edit' % u.user_name)
        
        if u.user_name in admins and len(admins) == 1:
            flash(_("Can not delete the only site administrator."), 'warning')
            redirect(came_from)
            
        confirmed = kw.get('confirmed', None)        
        if not confirmed:
            display_name = u.display_name
            action = url('/user/%s/delete' % u.user_name)
            return dict(errors={}, display_name=display_name, action=action, 
                        came_from=came_from)
        else:
            db.delete(u)
            transaction.commit()
            flash(_("%s and all associated data have been deleted." % \
                    _display_name), 'info')
            redirect(url('/logout_handler'))
