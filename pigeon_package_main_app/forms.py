from django import forms
from .models import Package

class NewPackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('name', 'is_public')