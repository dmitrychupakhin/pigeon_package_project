from django.db import models
from pigeon_package_account_app.models import PigeonPackageUser
from ckeditor.fields import RichTextField
from operator import attrgetter

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
    name = models.CharField(max_length=100, null=False, default='layer')
    picture = models.ImageField(upload_to=get_picture_object_filepath, null=True)
    x_position = models.IntegerField()
    y_position = models.IntegerField()
    order = models.PositiveIntegerField(default=0, null=False)
    
    def save(self, *args, **kwargs):
        # Combine 'layer' and 'order' to create the 'name'
        self.name = f'layer{self.order}'

        super().save(*args, **kwargs)

class TextObject(models.Model):
    name = models.CharField(max_length=100, null=False, default='layer')
    content = models.TextField()
    x_position = models.IntegerField()
    y_position = models.IntegerField()
    order = models.PositiveIntegerField(default=0, null=False)
    
    def save(self, *args, **kwargs):
        # Combine 'layer' and 'order' to create the 'name'
        self.name = f'layer{self.order}'

        super().save(*args, **kwargs)

class File(models.Model):
    
    name = models.CharField(max_length=100)
    width = models.IntegerField(default=1100)
    height = models.IntegerField(default=2200)
    package = models.ForeignKey('Package', on_delete=models.CASCADE, related_name='files')
    
    picture_objects = models.ManyToManyField('PictureObject', related_name='picture_objects')
    text_objects = models.ManyToManyField('TextObject', related_name='text_objects')
    
    def add_text_object(self, object, order):
        object.order = order
        
        all_objects = self.get_layers()
        
        insertion_index = 0
        for obj in all_objects:
            if obj.order < order:
                insertion_index += 1
            else:
                break
        
        for obj in all_objects[:insertion_index]:
            obj.order += 1
        
        for obj in all_objects:
            obj.save()  
        
        
        self.text_objects.add(object)
        self.save()
        
    
    def add_picture_object(self, object, order):
        object.order = order
        object.save()
        all_objects = self.get_layers()
        
        insertion_index = 0
        for obj in all_objects:
            if obj.order < order:
                insertion_index += 1
            else:
                break
        
        for obj in all_objects[insertion_index:]:
            obj.order += 1
        
        self.picture_objects.add(object)
        
        for obj in all_objects:
            obj.save()  
        
        self.save()
    
    def remove_text_object(self, text_object):
        order = text_object.order
        text_object.delete()  # Delete the text object

        # Update the order of remaining text objects
        for obj in self.text_objects.filter(order__gt=order):
            obj.order -= 1
            obj.save()

    def remove_picture_object(self, picture_object):
        order = picture_object.order
        picture_object.delete()  # Delete the picture object

        # Update the order of remaining picture objects
        for obj in self.picture_objects.filter(order__gt=order):
            obj.order -= 1
            obj.save()   
    
    def get_layers(self):
        all_objects = list(self.picture_objects.all()) + list(self.text_objects.all())
        all_objects = sorted(all_objects, key=attrgetter('order')) 
        return all_objects  
        
    
    def __str__(self):
        return f"Picture {self.id}"

