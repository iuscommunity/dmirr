
from django.contrib.auth.models import User
from django.db import models
from dmirr.hub.apps.projects.models import Project
from dmirr.hub.apps.archs.models import Arch
                                
class RepoManager(models.Manager):    
    def by_session(self, request, only_owned=False):
        Repos = []
        
        if not request.user.is_authenticated():
            return Repos
            
        if only_owned:
            return self.model.objects.all(user=request.user)
        else:
            _Repos = self.model.objects.all()
            for Repo in _Repos:
                if Repo.user == request.user:
                    Repos.append(Repo)
                    continue
                    
                for group in request.user.groups.all():
                    if group in Repo.groups:
                        Repos.append(Repo)
                        break
                        
        return Repos

        
class RepoBaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['label']
        
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True, auto_now=True)             
                        
class Repo(RepoBaseModel):
    class Meta:
        db_table = 'Repos'
        ordering = ['label']
          
    user = models.ForeignKey(User)
    label = models.CharField(max_length=128, blank=False, unique=True)
    display_name = models.CharField(max_length=256, blank=False, null=False)
    project = models.ForeignKey(Project, blank=False, 
                                related_name='repos')
    archs = models.ManyToManyField(Arch, blank=False, related_name='repos')
    path = models.CharField(max_length=255, blank=False)
    objects = RepoManager()

    def __unicode__(self):
        return unicode(self.display_name)
    
    def __str__(self):
        return self.display_name