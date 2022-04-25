
from django.urls import path

from .views import Dashboard, UserEditView, invite_code


urlpatterns = [
    
        path('', Dashboard, name='dashboard'),
        path('profile/', UserEditView.as_view(), name='profile'),
        path('invite-code/', invite_code, name='invite-code')
]
