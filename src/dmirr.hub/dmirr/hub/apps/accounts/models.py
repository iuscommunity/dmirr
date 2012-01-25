
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db import models
from userena.models import UserenaBaseProfile
from guardian.shortcuts import get_objects_for_user

from dmirr.hub.apps.projects.models import Project

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    
    @property
    def display_name(self):
        if self.user.first_name and self.user.last_name:
            return "%s %s" % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username

    @property
    def projects(self):
        set = get_objects_for_user(self.user, 'projects.change_project')
        return set
    
    @property
    def systems(self):
        set = get_objects_for_user(self.user, 'systems.change_system')
        return set

    @property
    def managed_groups(self):
        set = get_objects_for_user(self.user, 'auth.change_group')
        return set
    
    @property
    def unmanaged_groups(self):
        set = []
        for group in self.user.groups.all():
            if group not in self.managed_groups:
                set.append(group)
        return set
    