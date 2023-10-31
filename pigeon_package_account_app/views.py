from django.shortcuts import render
from django.http import HttpResponse

def registration(request):
    return render(request=request, template_name='pigeon_package_account_app/registration.html')

def authentication(request):
    return render(request=request, template_name='pigeon_package_account_app/authentication.html')