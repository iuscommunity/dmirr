
from django.contrib.auth.models import User, Group
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
            return self.model.objects.all(owner=request.user)
        else:
            _projects = self.model.objects.all()
            for project in _projects:
                if project.owner == request.user:
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
            
    owner = models.ForeignKey(User, related_name='projects')
    label = models.CharField(max_length=128, blank=False)
    display_name = models.CharField(max_length=256, blank=False)
    groups = models.ManyToManyField(Group, related_name='projects')
    description = models.TextField(blank=True)
    url = models.CharField(max_length=256, blank=True)
    private = models.BooleanField()
    objects = ProjectManager()
        
