from django.conf import settings
from django.shortcuts import render

def main(request):
    return render(request=request, template_name='pigeon_package_main_app/main-new-project.html', context={'MEDIA_URL': settings.MEDIA_URL})
