from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from pigeon_package_account_app.forms import RegistrationUserForm, AuthenticationUserForm, AccountUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os

from pigeon_package_account_app.models import PigeonPackageUser

class RegistrationUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'pigeon_package_account_app/registration.html'
    success_url = reverse_lazy('main')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form(self.form_class)
        return context
    
    def get_success_url(self):
        return reverse_lazy('authentication')
    
    

class AuthenticationUser(LoginView):
    form_class = AuthenticationUserForm
    template_name = 'pigeon_package_account_app/authentication.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form(self.form_class)
        return context
    
    def get_success_url(self):
        return reverse_lazy('main')
    
def deauthentication(request):
    logout(request)
    return redirect('authentication')

@login_required
def profile(request):
    user = request.user
    context = {}
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user, request=request)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": user.pk,
					"email": user.email, 
					"username": user.username,
					"profile_picture": user.profile_picture,
				}
			)
            context['form'] = form
    else:
        form = AccountUpdateForm(
			initial={
					"id": user.pk,
					"email": user.email, 
					"username": user.username,
					"profile_picture": user.profile_picture,
				}
			)
        context['form'] = form
        context['MEDIA_URL'] = settings.MEDIA_URL
    return render(request=request, template_name='pigeon_package_account_app/profile.html', context=context)