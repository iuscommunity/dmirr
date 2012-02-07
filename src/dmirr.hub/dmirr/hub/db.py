
from django.db import models
from tastypie.models import create_api_key

from django.contrib.auth.models import User, Group, Permission
from dmirr.hub.apps.accounts.models import UserProfile
from dmirr.hub.apps.projects.models import Project
from dmirr.hub.apps.repos.models import Repo
from dmirr.hub.apps.archs.models import Arch
from dmirr.hub.apps.protocols.models import Protocol
from dmirr.hub.apps.systems.models import System, SystemResource

models.signals.post_save.connect(create_api_key, sender=User)
