from django.urls import path
from authentication.Views.UserAccount import UserAccountView
from authentication.Views.UserLogin import Login
from authentication.Views.PasswordManagement import ChangePassword

urlpatterns = [
    path('login/', Login.as_view()),
    path('user_account/', UserAccountView.as_view()),
    path('change_password', ChangePassword.as_view()),
]