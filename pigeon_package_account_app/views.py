from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from pigeon_package_account_app.forms import RegistrationUserForm, AuthenticationUserForm
from django.contrib.auth.views import LoginView

def registration(request):
    return render(request=request, template_name='pigeon_package_account_app/registration.html')

def authentication(request):
    return render(request=request, template_name='pigeon_package_account_app/authentication.html')

class RegistrationUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'pigeon_package_account_app/registration.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save(commit=False)
        if 'profile_picture' in self.request.FILES:
            user.profile_picture = self.request.FILES['profile_picture']
        user.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form(self.form_class)
        return context

class AuthenticationUser(LoginView):
    form_class = AuthenticationUserForm
    template_name = 'pigeon_package_account_app/authentication.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form(self.form_class)
        return context
    
    def get_success_url(self):
        return reverse_lazy('main')