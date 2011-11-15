
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db import models
from userena.models import UserenaBaseProfile

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
