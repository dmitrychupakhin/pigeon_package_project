from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PigeonPackageUser
from django import forms

class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.TextInput(attrs={'class': 'form-input'}))
    profile_picture = forms.ImageField(label='Изображение профиля', required=False)
    
    class Meta:
        model = PigeonPackageUser
        fields = ('username', 'email', 'password1', 'password2', 'profile_picture')
        
class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = PigeonPackageUser
        fields = ['profile_picture', 'username', 'email', 'password']