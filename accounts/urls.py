from django.urls import path
from accounts.views import UserRegisterView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_registration'),
]
