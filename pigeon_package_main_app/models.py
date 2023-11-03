from django.db import models
from pigeon_package_account_app.models import PigeonPackageUser

class Package(models.Model):
    is_public = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(PigeonPackageUser, related_name='folders')
    
class TextFile(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    folder = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='files')

    class Meta:
        unique_together = ('name', 'folder',)
