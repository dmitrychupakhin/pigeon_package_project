from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('authentication/', authentication, name='authentication')
]