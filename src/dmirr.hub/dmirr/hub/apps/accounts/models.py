
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
    def my_projects(self):
        set = get_objects_for_user(self.user, 'projects.change_project')
        return set
    
    @property
    def my_systems(self):
        set = get_objects_for_user(self.user, 'systems.change_system')
        return set