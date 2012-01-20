
from django.db import models
        
class Protocol(models.Model):
    class Meta:
        db_table = 'protocols'
        ordering = ['label']
        
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True, auto_now=True)                     
    label = models.CharField(max_length=128, blank=False, unique=True)
    port = models.IntegerField()
    
    def __unicode__(self):
        return unicode(self.label)
    
    def __str__(self):
        return self.label