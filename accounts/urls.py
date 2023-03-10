from django.urls import path
from accounts.views import UserRegisterView, CreateCompanView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_registration'),
    path('create-company/', CreateCompanView.as_view(), name='create_company'),
]
