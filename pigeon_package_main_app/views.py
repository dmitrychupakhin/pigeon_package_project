from django.conf import settings
from django.shortcuts import redirect, render
from .forms import *
from .models import Package, TextFile
from django.contrib.auth.decorators import login_required

def file_editor(request, id):
    files = TextFile.objects.all()
    file = files.get(id=id)
    package = file.package
    form = FileEditForm(instance=file)
    context = {
        'form': form,
        'package': package,
        'files': files,
        'file': file,
        'MEDIA_URL': settings.MEDIA_URL
    }   
         
    if request.method == 'POST':
        form = FileEditForm(request.POST, instance=file)
        if form.is_valid():
            print(form)
            form.save()
            context['form'] = form
        print(form.errors)
    
    return render(request=request, template_name='pigeon_package_main_app/file-editor.html', context=context)

@login_required
def package_editor(request, id):
    user = request.user
    package = Package.objects.get(id=id)
    files = TextFile.objects.filter(package=id)
    
    context = {}
    
    if request.method == 'POST':
        form = NewFileForm(request.POST)
        if form.is_valid():
            package = Package.objects.get(id=id)
            file = form.save(package=package)
            return redirect('package-editor-page',id=id)
        else:
            context['form'] = form
    else:
        form = NewFileForm()
        context['form'] = form
    
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['files'] = files
    context['package'] = package
    
    return render(request=request, template_name='pigeon_package_main_app/package-editor.html', context=context)

@login_required
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