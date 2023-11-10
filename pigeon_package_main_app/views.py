from django.conf import settings
from django.shortcuts import redirect, render
from .forms import *
from .models import Package, TextFile, PackageInvitation
from django.contrib.auth.decorators import login_required

@login_required
def file_editor(request, id):
    file = TextFile.objects.get(id=id)
    package = file.package
    files = TextFile.objects.filter(package=package)
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
            form.save()
            context['form'] = form
    
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

@login_required
def new_package(request):
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
    
    return render(request=request, template_name='pigeon_package_main_app/new-package.html', context=context)

@login_required
def remove_package(request):
    user = request.user
    packages = Package.objects.filter(users=user)
    
    context = {}
    
    if request.method == 'POST':
        form = RemovePackageForm(request.POST, user=user)
        if form.is_valid():
            packages_to_delete = form.cleaned_data['packages']
            for package_to_delete in packages_to_delete:
                package_to_delete.users.remove(user)
                if package_to_delete.users.count() == 0:
                    package_to_delete.delete()
            
            return redirect('main')
        else:
            context['form'] = form
    else:
        form = RemovePackageForm(user=user)
        context['form'] = form
    
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['packages'] = packages
    
    return render(request=request, template_name='pigeon_package_main_app/remove-package.html', context=context)

@login_required
def new_file(request, id):
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
    
    return render(request=request, template_name='pigeon_package_main_app/new-file.html', context=context)

@login_required
def remove_file(request, id):
    
    user = request.user
    package = Package.objects.get(id=id)
    files = TextFile.objects.filter(package=id)
    
    context = {}
    
    if request.method == 'POST':
        form = RemoveFileForm(request.POST, package=package)
        if form.is_valid():
            files_to_delete = form.cleaned_data['files']
            files_to_delete.delete()
            return redirect('package-editor-page', id)
        else:
            context['form'] = form
    else:
        form = RemoveFileForm( package=package)
        context['form'] = form
    
    context['package'] = package
    context['MEDIA_URL'] = settings.MEDIA_URL
    context['files'] = files
    
    return render(request=request, template_name='pigeon_package_main_app/remove-file.html', context=context)   

@login_required
def invitations(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL
    }
    return render(request=request, template_name='pigeon_package_main_app/invitations.html', context=context)

@login_required
def incoming_invitations(request):
    user = request.user
    invitations = PackageInvitation.objects.filter(recipient=user)
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'invitations': invitations
    }
    return render(request=request, template_name='pigeon_package_main_app/incoming-invitations.html', context=context)

@login_required
def outgoing_invitations(request):
    user = request.user
    invitations = PackageInvitation.objects.filter(sender=user)
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'invitations': invitations
    }
    return render(request=request, template_name='pigeon_package_main_app/outgoing-invitations.html', context=context)

@login_required
def new_invitation(request, id):
    user = request.user
    package = Package.objects.get(id=id)
    files = TextFile.objects.filter(package=id)
    context = {}
    context['package'] = package
    context['files'] = files
    context['MEDIA_URL'] = settings.MEDIA_URL
    
    if request.method == 'POST':
        form = PigeonPackageUserGetForm(request.POST)
        if form.is_valid():
            recipient = PigeonPackageUser.objects.get(username=form.cleaned_data['username']) 
            invitation = PackageInvitation(
            package=package,
            sender=user,
            recipient=recipient,
            is_accepted=False)
            
            if (PackageInvitation.objects.filter(package=package, sender=user, recipient=recipient)) or (user == recipient) or package.users.filter(id=recipient.id):
                return redirect('new-invitation', id)
            else:
                invitation.save()
            return redirect('new-invitation', id)  # Перенаправляем на страницу успеха или другую страницу
        else:
            context['form'] = form
    else:
        form = PigeonPackageUserGetForm()
        context['form'] = form
    
    return render(request, 'pigeon_package_main_app/package-new-invitation.html', context)

@login_required
def accept_invitation(request, id):
    invitation = PackageInvitation.objects.get(id=id)
    package = invitation.package
    package.users.add(invitation.recipient)
    invitation.delete()
    return redirect('incoming_invitations')

@login_required
def reject_invitation_incoming(request, id):
    invitation = PackageInvitation.objects.get(id=id)
    invitation.delete()
    return redirect('incoming_invitations')

@login_required
def reject_invitation_outgoing(request, id):
    invitation = PackageInvitation.objects.get(id=id)
    invitation.delete()
    return redirect('outgoing_invitations')

@login_required
def package_settings(request, id):
    user = request.user
    package = Package.objects.get(id=id)
    
    context = {
        'package': package
    }
    context['MEDIA_URL'] = settings.MEDIA_URL
    
    if request.method == 'POST':
        form = SettigsPackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
        else:
            context['form'] = form
        return redirect('package-settings', id) 
    else:
        context['form'] = SettigsPackageForm(instance=package)
    
    return render(request, 'pigeon_package_main_app/package-settings.html', context)