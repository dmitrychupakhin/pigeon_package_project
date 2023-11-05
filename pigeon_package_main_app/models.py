from django.db import models
from pigeon_package_account_app.models import PigeonPackageUser

class Package(models.Model):
    is_public = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(PigeonPackageUser, related_name='packages')
    def __str__(self):
        return self.name
    
class TextFile(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='files')
    font_size = models.PositiveIntegerField(default=12, null=True)
    
    class Meta:
        unique_together = ('name', 'package',)
        
    
