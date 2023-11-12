from django import forms
from .models import *
from django.core.exceptions import ValidationError

class FileEditForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'myTextarea editor__text-area', 'id': 'myTextarea'}), required=False, strip=False)
    
    class Meta:
        model = TextFile
        fields = ('content',)

class NewPackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('name', 'is_public')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'my-input-class'}),
        }

class SettigsPackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('name', 'is_public')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'my-input-class'}),
        }
        
class ManageUsersPackageForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=PigeonPackageUser.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    def __init__(self, *args, **kwargs):
        package_id = kwargs.pop('package_id', None)
        super(ManageUsersPackageForm, self).__init__(*args, **kwargs)

        if package_id is not None:
            # Фильтруем queryset только для пользователей, владеющих данным пакетом
            self.fields['users'] = forms.ModelMultipleChoiceField(
                queryset=PigeonPackageUser.objects.filter(packages__id=package_id),
                widget=forms.CheckboxSelectMultiple(),
            )

class RemovePackageForm(forms.Form):
    packages = forms.ModelMultipleChoiceField(queryset=Package.objects.all(), widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлечение пользователя из kwargs
        super(RemovePackageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['packages'].queryset = Package.objects.filter(users=user)

class RemoveFileForm(forms.Form):
    files = forms.ModelMultipleChoiceField(queryset=TextFile.objects.all(), widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        package = kwargs.pop('package', None)  # Извлечение пользователя из kwargs
        super(RemoveFileForm, self).__init__(*args, **kwargs)
        if package:
            self.fields['files'].queryset = TextFile.objects.filter(package=package)
            
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
    
class PigeonPackageUserGetForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not PigeonPackageUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь не найден")
        return username