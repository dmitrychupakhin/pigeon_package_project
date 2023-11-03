from django.conf import settings
from django.shortcuts import redirect, render
from .forms import *
from .models import Package

def package_editor(request, id):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request=request, template_name='pigeon_package_main_app/package-editor.html', context=context)

def main(request):
    user = request.user
    packages = Package.objects.filter(users=user)
    
    context = {}
    
    if request.method == 'POST':
        form = NewPackageForm(request.POST)
        if form.is_valid():
            package = form.save()
            package.users.add(request.user)
            return redirect('main')
        else:
            context['form'] = form
    else:
        form = NewPackageForm()
        context['form'] = form
    
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['packages'] = packages
    return render(request=request, template_name='pigeon_package_main_app/main.html', context=context)