
from django.db import models
from tastypie.models import create_api_key

from django.contrib.auth.models import User, Group, Permission
from dmirr.hub.apps.accounts.models import UserProfile
from dmirr.hub.apps.projects.models import Project

models.signals.post_save.connect(create_api_key, sender=User)
