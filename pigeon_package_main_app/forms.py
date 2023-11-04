from django import forms
from .models import Package, TextFile

class NewPackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('name', 'is_public')
        
class NewFileForm(forms.ModelForm):
    class Meta:
        model = TextFile
        fields = ('name',)
    def save(self, package=None, commit=True):
        instance = super(NewFileForm, self).save(commit=False)
        if package is not None:
            instance.package = package
        if commit:
            instance.save()
        return instance