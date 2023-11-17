from django.db import models
from pigeon_package_account_app.models import PigeonPackageUser
from ckeditor.fields import RichTextField

class Package(models.Model):
    is_public = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(PigeonPackageUser, related_name='packages')
    def __str__(self):
        return self.name

class PackageInvitation(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    sender = models.ForeignKey(PigeonPackageUser, on_delete=models.CASCADE, related_name='invitations_sent')
    recipient = models.ForeignKey(PigeonPackageUser, on_delete=models.CASCADE, related_name='invitations_received')
    is_accepted = models.BooleanField(default=False)

def get_picture_object_filepath(self, filename):
	return 'file_picture/' + str(self.pk) + '/' + filename + '.png'

class PictureObject(models.Model):
    picture = models.ImageField(upload_to=get_picture_object_filepath, null=True)
    x_position = models.IntegerField()
    y_position = models.IntegerField()

class TextObject(models.Model):
    content = models.TextField()
    x_position = models.IntegerField()
    y_position = models.IntegerField()

class File(models.Model):
    
    name = models.CharField(max_length=100)
    width = models.IntegerField(default=1100)
    height = models.IntegerField(default=2200)
    picture_objects = models.ManyToManyField('PictureObject', related_name='picture_objects')
    text_objects = models.ManyToManyField('TextObject', related_name='text_objects')
    package = models.ForeignKey('Package', on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f"Picture {self.id}"

