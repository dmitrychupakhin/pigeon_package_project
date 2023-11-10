from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('new-package/', new_package, name='new-package'),
    path('package-editor-page/<int:id>', package_editor ,name='package-editor-page'),
    path('file-editor-page/<int:id>', file_editor ,name='file-editor-page'),
    path('remove-package/', remove_package, name='remove-package'),
    path('file-editor-page/<int:id>/new-file/', new_file, name='new-file'),
    path('file-editor-page/<int:id>/remove-file/', remove_file, name='remove-file'),
    path('invitations', invitations, name='invitations'),
    path('incoming-invations', incoming_invitations, name='incoming_invitations'),
    path('outgoing_invitations', outgoing_invitations, name='outgoing_invitations'),
    path('package-editor-page/<int:id>/new-invitation', new_invitation, name='new-invitation'),
    path('accept_invitation/<int:id>', accept_invitation, name='accept_invitation'),
    path('reject_invitation_incoming/<int:id>', reject_invitation_incoming, name='reject_invitation_incoming'),
    path('reject_invitation_outgoing/<int:id>', reject_invitation_outgoing, name='reject_invitation_outgoing'),
    path('package-settings/<int:id>', package_settings, name='package-settings'),
]