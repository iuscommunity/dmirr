
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django.db import models

from dmirr.hub.apps.archs.models import Arch

class Project(models.Model):
    class Meta:
        db_table = 'projects'
            
    user = models.ForeignKey(User, related_name='projects')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True, auto_now=True)
    label = models.CharField(max_length=128, blank=False, unique=True)
    display_name = models.CharField(max_length=256, blank=False, null=False)
    admin_group = models.ForeignKey(Group, related_name='projects', null=True, blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=256, blank=True)
    private = models.BooleanField()
        
    def __repr__(self):
        return self.display_name
    
    def __unicode__(self):
        return unicode(self.display_name)
                                              
class ProjectRepo(models.Model):
    class Meta:
        db_table = 'project_repos'
        ordering = ['label']
          
    user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True, auto_now=True)             
    label = models.CharField(max_length=128, blank=False, unique=True)
    display_name = models.CharField(max_length=256, blank=False, null=False)
    project = models.ForeignKey(Project, blank=False, 
                                related_name='repos')
    archs = models.ManyToManyField(Arch, blank=False, related_name='repos')
    path = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return unicode(self.display_name)
    
    def __str__(self):
        return self.display_name