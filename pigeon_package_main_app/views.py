from django.shortcuts import render

def main(request):
    return render(request=request, template_name='pigeon_package_main_app/main.html')
