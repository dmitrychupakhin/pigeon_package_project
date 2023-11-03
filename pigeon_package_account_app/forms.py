from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from .models import *
from django import forms

class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.TextInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = PigeonPackageUser
        fields = ('username', 'email', 'password1', 'password2')
        
class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class AccountUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
    
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
    confirm_new_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = PigeonPackageUser
        fields = ('username', 'email', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = PigeonPackageUser.objects.exclude(pk=self.instance.pk).get(email=email)
        except PigeonPackageUser.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = PigeonPackageUser.objects.exclude(pk=self.instance.pk).get(username=username)
        except PigeonPackageUser.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)
    
    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "Passwords do not match.")
        if current_password and not self.instance.check_password(current_password):
            self.add_error('current_password', "Incorrect current password.")

        return cleaned_data
    
    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_picture = self.cleaned_data['profile_picture']
        
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            account.set_password(new_password)
            account.save()
            update_session_auth_hash(self.request, account)
        
        if commit:
            account.save()
        return account