from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('authentication/', AuthenticationUser.as_view(), name='authentication'),
    path('deauthentication/', deauthentication, name='deauthentication'),
    path('profile', profile, name='profile')
]