
from django.db import models
from tastypie.models import create_api_key

from django.contrib.auth.models import User, Group, Permission
from dmirr.hub.apps.accounts.models import UserProfile

models.signals.post_save.connect(create_api_key, sender=User)
