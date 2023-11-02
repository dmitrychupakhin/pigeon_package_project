from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('authentication/', authentication, name='authentication')
]