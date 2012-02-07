
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django.db import models

    
class ProjectBaseModel(models.Model):
    class Meta:
        abstract = True
        
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True, auto_now=True)
    
class ProjectManager(models.Manager):    
    def by_session(self, request, only_owned=False):
        projects = []
        
        if not request.user.is_authenticated():
            return projects
            
        if only_owned:
            return self.model.objects.all(user=request.user)
        else:
            _projects = self.model.objects.all()
            for project in _projects:
                if project.user == request.user:
                    projects.append(project)
                    continue
                    
                for group in request.user.groups.all():
                    if group in project.groups:
                        projects.append(project)
                        break
                        
        return projects                  
                        
class Project(ProjectBaseModel):
    class Meta:
        db_table = 'projects'
            
    user = models.ForeignKey(User, related_name='projects')
    label = models.CharField(max_length=128, blank=False, unique=True)
    display_name = models.CharField(max_length=256, blank=False, null=False)
    admin_group = models.ForeignKey(Group, related_name='projects', null=True, blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=256, blank=True)
    private = models.BooleanField()
    objects = ProjectManager()
        
    def __repr__(self):
        return self.display_name
    
    def __unicode__(self):
        return unicode(self.display_name)
        
#@receiver(post_save, sender=ProjectItemContribution)
#def create_allocations_with_contrib(sender, **kw):
#    # only for new records
#    if not kw['created']:
#        return
