from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('package-editor-page/<int:id>', package_editor ,name='package-editor-page'),
    path('file-editor-page/<int:id>', file_editor ,name='file-editor-page')
]