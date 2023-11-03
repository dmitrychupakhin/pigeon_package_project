from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from pigeon_package_account_app.forms import RegistrationUserForm, AuthenticationUserForm, UserEditForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
import os
from .models import *

from pigeon_package_account_app.models import PigeonPackageUser

class RegistrationUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'pigeon_package_account_app/registration.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save(commit=False)
        
        user.save()
        
        if 'profile_picture' in self.request.FILES:
            uploaded_file = self.request.FILES['profile_picture']
        
            # Путь к папке для сохранения изображений пользователя
            user_image_path = os.path.join(settings.MEDIA_ROOT, 'user_picture', str(user.id))
            
            # Создание папки для изображений пользователя, если её нет
            os.makedirs(user_image_path, exist_ok=True)

            # Путь к файлу изображения пользователя
            user_image_file_path = os.path.join(user_image_path, 'profile.jpg')  # или другое расширение файла

            # Сохранение изображения по указанному пути
            with open(user_image_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Сохранение пути к изображению в поле профиля пользователя
            user.profile_picture = os.path.join('user_picture', str(user.id), 'profile.jpg')
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
    
def deauthentication(request):
    logout(request)
    return redirect('authentication')

def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            if 'profile_picture' in request.FILES:
                uploaded_file = request.FILES['profile_picture']
            
                # Путь к папке для сохранения изображений пользователя
                user_image_path = os.path.join(settings.MEDIA_ROOT, 'user_picture', str(user.id))
                
                # Создание папки для изображений пользователя, если её нет
                os.makedirs(user_image_path, exist_ok=True)

                # Путь к файлу изображения пользователя
                user_image_file_path = os.path.join(user_image_path, 'profile.jpg')  # или другое расширение файла

                # Сохранение изображения по указанному пути
                with open(user_image_file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Сохранение пути к изображению в поле профиля пользователя
                user.profile_picture = os.path.join('user_picture', str(user.id), 'profile.jpg')
                user.save()
            else:
                user.profile_picture = get_default_profile_image()
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=user)
    
    context={'MEDIA_URL': settings.MEDIA_URL,
             'form': form}
    return render(request=request, template_name='pigeon_package_account_app/profile.html', context=context)