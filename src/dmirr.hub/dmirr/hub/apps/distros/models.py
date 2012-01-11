
from django.contrib.auth.models import User
from django.db import models
from dmirr.hub.apps.projects.models import Project

class DistroManager(models.Manager):    
    def by_session(self, request, only_owned=False):
        distros = []
        
        if not request.user.is_authenticated():
            return distros
            
        if only_owned:
            return self.model.objects.all(user=request.user)
        else:
            _distros = self.model.objects.all()
            for distro in _distros:
                if distro.user == request.user:
                    distros.append(distro)
                    continue
                    
                for group in request.user.groups.all():
                    if group in distro.groups:
                        distros.append(distro)
                        break
                        
        return distros

        
class DistroBaseModel(models.Model):
    class Meta:
        abstract = True
        
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True, auto_now=True)             
                        
class Distro(DistroBaseModel):
    class Meta:
        db_table = 'distros'
            
    user = models.ForeignKey(User, related_name='distros')
    label = models.CharField(max_length=128, blank=False, unique=True)
    display_name = models.CharField(max_length=256, blank=False, null=False)
    distro = models.ForeignKey(Project, blank=False, 
                                related_name='distros')
    objects = DistroManager()