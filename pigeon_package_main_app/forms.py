from django import forms
from .models import Package, TextFile

class FileEditForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'myTextarea editor__text-area', 'id': 'myTextarea'}), required=False, strip=False)
    font_size = forms.IntegerField(label='Font Size', required=False, widget=forms.HiddenInput(attrs={'id': 'font_size'}))
    
    class Meta:
        model = TextFile
        fields = ('content','font_size',)
        
    def __init__(self, *args, **kwargs):
        super(FileEditForm, self).__init__(*args, **kwargs)
        
        instance = kwargs.get('instance')
        font_size = instance.font_size

        self.fields['content'].widget.attrs.update({'style': f'font-size: {font_size}px;'})

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